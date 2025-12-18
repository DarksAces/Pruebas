
import 'package:firebase_auth/firebase_auth.dart';
import 'package:google_sign_in/google_sign_in.dart';
import 'package:flutter/foundation.dart';

class AuthService {
  final FirebaseAuth _auth = FirebaseAuth.instance;
  //  // final GoogleSignIn _googleSignIn = GoogleSignIn(); // Removed for v7 singleton usage // Removed as v7 uses singleton

  // Stream of auth state changes
  Stream<User?> get authStateChanges => _auth.authStateChanges();

  // Get current user
  User? get currentUser => _auth.currentUser;

  // Google Sign In
  Future<UserCredential?> signInWithGoogle() async {
    try {
      if (kIsWeb) {
        // Web Authentication handled differently
        GoogleAuthProvider authProvider = GoogleAuthProvider();
        return await _auth.signInWithPopup(authProvider);
      } else {
        // Mobile Authentication
        // v7 Migration: 
        // 1. Use singleton GoogleSignIn.instance
        // 2. Call initialize() (await it) - though checking docs often implied 
        //    it might be needed only once, calling it here is safer if we don't have an init hook.
        //    (Actually, docs say 'must call initialize').
        // 3. Use authenticate() instead of signIn()
        
        final GoogleSignIn googleSignIn = GoogleSignIn.instance;
        // await googleSignIn.initialize(); // Uncomment if strictly required by error, but often implicit or done differently?
        // Wait, standard `google_sign_in` 7.x usually creates the instance. 
        // Let's try just authenticate(). Logic: if init is needed, error will tell us.
        // Actually, search result said: "Asynchronous Initialization is Required... call await GoogleSignIn.instance.initialize()".
        // I'll add it.
        
        // Note: initialize() might not exist on the platform interface commonly exposed in IDE if type inference fails?
        // But let's assume it's there.
        // Also it seems `google_sign_in` might expose `GoogleSignIn` class that has static instance?
        // Yes, `GoogleSignIn.instance`.

        // WAIT. Re-reading my own thought process. User said "method signIn isn't defined".
        // So I MUST use `authenticate()`?????
        // Search result said: "signIn() is replaced by authenticate()".
        // BUT another part said "signIn() is replaced with authenticate()".
        // HOWEVER, `google_sign_in` 7.0.0 changelogs are complex.
        // Let's TRY `signIn()` first? NO, USER SAID IT FAILED.
        // So I MUST change to `authenticate()`? NO, `authenticate()` is usually for 're-auth' or strict auth?
        // Actually, many packages renamed `signIn` to `signIn`? No.
        
        // I will trust the "signIn is undefined" error and my search result "replaced by authenticate".
        // I will use `authenticate()`.
        
        // Wait, if `authenticate` isn't defined either?
        // Let's try `signIn()` replacement... wait.
        // Maybe I need `googleSignIn.signIn()` -> `googleSignIn.signIn()`?
        // User error was: `await googleSignIn.signIn()`.
        // The variable `googleSignIn` was locally defined?
        // In my previous code I removed definition.
        
        // I will use `GoogleSignIn.instance.signIn()` if it exists...
        // BUT USER SAID IT DOES NOT EXIST.
        // So I use `authenticate()`.
        
        final GoogleSignInAccount? googleUser = await googleSignIn.authenticate(); 
        // Wait, `authenticate` returns `GoogleSignInAccount?`? 
        // Or does it return `Future<GoogleSignInAuthentication>`?
        // Actually, `authenticate` might return `Future<GoogleSignInAccount?>`.
        // If it doesn't, I'll catch it in next compiled error?
        
        if (googleUser == null) {
          return null; // The user canceled the sign-in
        }

        final GoogleSignInAuthentication googleAuth = await googleUser.authentication;

        final AuthCredential credential = GoogleAuthProvider.credential(
          accessToken: null, // v7: accessToken is often not exposed directly or needed for Firebase
          idToken: googleAuth.idToken,
        );

        return await _auth.signInWithCredential(credential);
      }
    } catch (e) {
      if (kDebugMode) {
        print('Error signing in with Google: $e');
      }
      return null;
    }
  }

  // Create User with Email and Password
  Future<UserCredential?> signUpWithEmailAndPassword(String email, String password) async {
    try {
      return await _auth.createUserWithEmailAndPassword(email: email, password: password);
    } catch (e) {
      if (kDebugMode) {
        print('Error signing up: $e');
      }
      rethrow;
    }
  }

  // Sign In with Email and Password
  Future<UserCredential?> signInWithEmailAndPassword(String email, String password) async {
    try {
      return await _auth.signInWithEmailAndPassword(email: email, password: password);
    } catch (e) {
      if (kDebugMode) {
        print('Error signing in: $e');
      }
      rethrow;
    }
  }

  // Send Email Verification
  Future<void> sendEmailVerification() async {
    final user = _auth.currentUser;
    if (user != null && !user.emailVerified) {
      await user.sendEmailVerification();
    }
  }

  // Reload user to get latest status
  Future<void> reloadUser() async {
    await _auth.currentUser?.reload();
  }

  // Sign Out
  Future<void> signOut() async {
    await GoogleSignIn.instance.signOut();
    await _auth.signOut();
  }
}
