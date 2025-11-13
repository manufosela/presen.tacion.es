const FIREBASE_SDK_VERSION = "10.12.0";
const FIREBASE_APP_URL = `https://www.gstatic.com/firebasejs/${FIREBASE_SDK_VERSION}/firebase-app.js`;
const FIREBASE_AUTH_URL = `https://www.gstatic.com/firebasejs/${FIREBASE_SDK_VERSION}/firebase-auth.js`;
const FIREBASE_FIRESTORE_URL = `https://www.gstatic.com/firebasejs/${FIREBASE_SDK_VERSION}/firebase-firestore.js`;

let firebaseContextPromise = null;

async function loadFirebaseConfig() {
  try {
    const configModule = await import("../firebase-config.js");
    return configModule.default || configModule.firebaseConfig || null;
  } catch (error) {
    console.warn(
      "[firebase] Configuración no encontrada. Copia firebase-config.example.js a firebase-config.js y añade tus valores."
    );
    return null;
  }
}

async function bootstrapFirebase() {
  const config = await loadFirebaseConfig();
  if (!config) {
    return null;
  }

  const [appModule, authModule, firestoreModule] = await Promise.all([
    import(FIREBASE_APP_URL),
    import(FIREBASE_AUTH_URL),
    import(FIREBASE_FIRESTORE_URL),
  ]);

  const { initializeApp } = appModule;
  const {
    getAuth,
    GoogleAuthProvider,
    signInWithPopup,
    signOut,
    onAuthStateChanged,
    setPersistence,
    browserLocalPersistence,
  } = authModule;
  const {
    getFirestore,
    doc,
    collection,
    setDoc,
    getDoc,
    getDocs,
    updateDoc,
    serverTimestamp,
    onSnapshot,
    query,
    orderBy,
    limit,
    deleteDoc,
  } = firestoreModule;

  const app = initializeApp(config);
  const auth = getAuth(app);
  await setPersistence(auth, browserLocalPersistence);
  const db = getFirestore(app);

  return {
    app,
    auth,
    db,
    modules: {
      GoogleAuthProvider,
      signInWithPopup,
      signOut,
      onAuthStateChanged,
      doc,
      collection,
      setDoc,
      getDoc,
      getDocs,
      updateDoc,
      serverTimestamp,
      onSnapshot,
      query,
      orderBy,
      limit,
      deleteDoc,
    },
  };
}

async function ensureContext() {
  if (!firebaseContextPromise) {
    firebaseContextPromise = bootstrapFirebase();
  }
  return firebaseContextPromise;
}

export async function initFirebase() {
  return ensureContext();
}

export async function onAuthState(callback) {
  const context = await ensureContext();
  if (!context) {
    callback(null);
    return () => {};
  }
  return context.modules.onAuthStateChanged(context.auth, callback);
}

export async function signInWithGoogle() {
  const context = await ensureContext();
  if (!context) {
    throw new Error("Firebase no está configurado.");
  }
  const provider = new context.modules.GoogleAuthProvider();
  provider.setCustomParameters({ prompt: "select_account" });
  return context.modules.signInWithPopup(context.auth, provider);
}

export async function signOutUser() {
  const context = await ensureContext();
  if (!context) {
    return;
  }
  await context.modules.signOut(context.auth);
}

export async function getCurrentUser() {
  const context = await ensureContext();
  return context?.auth?.currentUser ?? null;
}

export async function savePresentationForUser(user, presentation, existingId) {
  const context = await ensureContext();
  if (!context) {
    throw new Error("Firebase no está configurado.");
  }

  const { db, modules } = context;
  const colRef = modules.collection(db, "users", user.uid, "presentations");
  const docRef =
    existingId != null
      ? modules.doc(colRef, existingId)
      : modules.doc(colRef);

  const timestamps = existingId
    ? { updatedAt: modules.serverTimestamp() }
    : {
        createdAt: modules.serverTimestamp(),
        updatedAt: modules.serverTimestamp(),
      };

  await modules.setDoc(
    docRef,
    {
      ownerUid: user.uid,
      ...presentation,
      ...timestamps,
    },
    { merge: true }
  );

  return docRef.id;
}

export async function fetchUserPresentation(ownerUid, presentationId) {
  const context = await ensureContext();
  if (!context) {
    throw new Error("Firebase no está configurado.");
  }

  const { db, modules } = context;
  const docRef = modules.doc(
    db,
    "users",
    ownerUid,
    "presentations",
    presentationId
  );
  const snapshot = await modules.getDoc(docRef);
  if (!snapshot.exists()) {
    return null;
  }
  return { id: snapshot.id, ...snapshot.data() };
}

export async function subscribeToUserPresentations(
  ownerUid,
  callback,
  options = {}
) {
  const context = await ensureContext();
  if (!context) {
    callback([]);
    return () => {};
  }

  const { db, modules } = context;
  const colRef = modules.collection(db, "users", ownerUid, "presentations");

  let q = colRef;
  if (options.orderByUpdatedAt !== false) {
    q = modules.query(colRef, modules.orderBy("updatedAt", "desc"), modules.limit(50));
  }

  return modules.onSnapshot(
    q,
    (snapshot) => {
      const items = snapshot.docs.map((docSnap) => ({
        id: docSnap.id,
        ...docSnap.data(),
      }));
      callback(items);
    },
    (error) => {
      console.error("Error al suscribirse a presentaciones:", error);
      callback([]);
    }
  );
}

export async function deleteUserPresentation(ownerUid, presentationId) {
  const context = await ensureContext();
  if (!context) {
    throw new Error("Firebase no está configurado.");
  }
  const { db, modules } = context;
  const docRef = modules.doc(
    db,
    "users",
    ownerUid,
    "presentations",
    presentationId
  );
  await modules.deleteDoc(docRef);
}

function buildSessionDocRef(modules, db, sessionKey) {
  return modules.doc(db, "sessions", sessionKey);
}

export async function listenToSession(sessionKey, callback) {
  const context = await ensureContext();
  if (!context) {
    callback(null);
    return () => {};
  }
  const { db, modules } = context;
  const docRef = buildSessionDocRef(modules, db, sessionKey);
  return modules.onSnapshot(
    docRef,
    (snapshot) => {
      if (snapshot.exists()) {
        callback({ id: snapshot.id, ...snapshot.data() });
      } else {
        callback(null);
      }
    },
    (error) => {
      console.error("Error escuchando sesión remota:", error);
      callback(null);
    }
  );
}

export async function upsertSession(sessionKey, data) {
  const context = await ensureContext();
  if (!context) {
    throw new Error("Firebase no está configurado.");
  }
  const { db, modules } = context;
  const docRef = buildSessionDocRef(modules, db, sessionKey);
  await modules.setDoc(
    docRef,
    { ...data, updatedAt: modules.serverTimestamp() },
    { merge: true }
  );
}

export async function updateSessionSlide(sessionKey, slideState) {
  const context = await ensureContext();
  if (!context) {
    throw new Error("Firebase no está configurado.");
  }
  const { db, modules } = context;
  const docRef = buildSessionDocRef(modules, db, sessionKey);
  await modules.setDoc(
    docRef,
    {
      currentSlide: slideState,
      updatedAt: modules.serverTimestamp(),
    },
    { merge: true }
  );
}

export async function clearSession(sessionKey) {
  const context = await ensureContext();
  if (!context) {
    return;
  }
  const { db, modules } = context;
  const docRef = buildSessionDocRef(modules, db, sessionKey);
  await modules.deleteDoc(docRef);
}
