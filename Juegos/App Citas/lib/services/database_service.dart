
import 'package:cloud_firestore/cloud_firestore.dart';
import '../models/models.dart' as app_models;

class DatabaseService {
  final FirebaseFirestore _db = FirebaseFirestore.instance;

  // Collection References
  CollectionReference get _usersRef => _db.collection('users');
  CollectionReference get _questionsRef => _db.collection('questions');

  // Ensure User Exists (Create if not, otherwise Update minimal info)
  Future<void> ensureUserExists(app_models.User user) async {
    final docRef = _usersRef.doc(user.id);
    final docSnapshot = await docRef.get();

    if (!docSnapshot.exists) {
      // New user, create full document
      await docRef.set(user.toMap());
    } else {
      // Existing user, mostly don't touch, maybe update push token or lastLogin
      // For now we do nothing or just ensure name/image is up to date if we wanted from Google
      // decided to NOT overwrite basic fields to respect user edits.
    }
  }

  // Save User (Create or Update)
  Future<void> saveUser(app_models.User user) async {
    await _usersRef.doc(user.id).set(user.toMap(), SetOptions(merge: true));
  }

  // Get All Users (Potential Matches)
  // In a real app we'd filter out the current user and maybe do pagination/geo rules
  Stream<List<app_models.User>> getUsers() {
    return _usersRef.snapshots().map((snapshot) {
      return snapshot.docs.map((doc) {
        return app_models.User.fromMap(doc.data() as Map<String, dynamic>, doc.id);
      }).toList();
    });
  }

  // Save a question to Firestore
  Future<void> saveQuestion(app_models.Question question) async {
    await _questionsRef.doc(question.id).set(question.toMap());
  }

  // Stream of questions for a specific user (Receiver)
  Stream<List<app_models.Question>> getQuestionsForUser(String userId) {
    return _questionsRef
        .where('receiverId', isEqualTo: userId)
        .orderBy('timestamp', descending: true)
        .snapshots()
        .map((snapshot) {
      return snapshot.docs.map((doc) {
        return app_models.Question.fromMap(doc.data() as Map<String, dynamic>, doc.id);
      }).toList();
    });
  }

  // Record a swipe (Like/Nope)
  Future<bool> recordSwipe(String userId, String targetUserId, bool isLike) async {
    try {
      // 1. Record the swipe in subcollection
      await _usersRef.doc(userId).collection('swipes').doc(targetUserId).set({
        'like': isLike,
        'timestamp': FieldValue.serverTimestamp(),
      });

      if (isLike) {
        // 2. Check for mutual like
        final targetSwipe = await _usersRef
            .doc(targetUserId)
            .collection('swipes')
            .doc(userId)
            .get();

        if (targetSwipe.exists) {
          final data = targetSwipe.data() as Map<String, dynamic>;
          if (data['like'] == true) {
            // It's a MATCH!
            await _createMatch(userId, targetUserId);
            return true; // Return true to indicate a match occurred
          }
        }
      }
    } catch (e) {
      print('Error recording swipe: $e');
    }
    return false;
  }

  // Create match document
  Future<void> _createMatch(String userA, String userB) async {
    // Generate a unique ID (lexicographically matched) so A-B and B-A are same doc
    final ids = [userA, userB]..sort();
    final matchId = ids.join('_');

    await _db.collection('matches').doc(matchId).set({
      'users': ids,
      'timestamp': FieldValue.serverTimestamp(),
    });
  }

  // Get Matches for a user
  // Returns a Stream of List<User> representing the matched profiles
  Stream<List<app_models.User>> getMatches(String userId) {
    return _db
        .collection('matches')
        .where('users', arrayContains: userId)
        .orderBy('timestamp', descending: true)
        .snapshots()
        .asyncMap((snapshot) async {
      final matchedUsers = <app_models.User>[];

      for (var doc in snapshot.docs) {
        final users = List<String>.from(doc['users']);
        final otherUserId = users.firstWhere((id) => id != userId);

        // Fetch user profile (future optimization: cache or separate stream)
        final userDoc = await _usersRef.doc(otherUserId).get();
        if (userDoc.exists) {
          matchedUsers.add(app_models.User.fromMap(
              userDoc.data() as Map<String, dynamic>, userDoc.id));
        }
      }
      return matchedUsers;
    });
  }
}
