
import 'package:cloud_firestore/cloud_firestore.dart';
import '../models/models.dart' as app_models;

class DatabaseService {
  final FirebaseFirestore _db = FirebaseFirestore.instance;

  // Collection References
  CollectionReference get _usersRef => _db.collection('users');
  CollectionReference get _questionsRef => _db.collection('questions');

  // Helper to convert Firestore Document to App User Model
  // Note: Model needs to be updated to have toMap/fromMap to be fully efficient,
  // but we will do manual mapping for now.

  Future<void> saveUser(app_models.User user) async {
    await _usersRef.doc(user.id).set({
      'name': user.name,
      'age': user.age,
      'bio': user.bio,
      'imageUrl': user.imageUrl,
      'photos': user.photos,
    }, SetOptions(merge: true)); // Merge prevents overwriting existing fields if we update partial data
  }

  // Save a question to Firestore
  Future<void> saveQuestion(app_models.Question question) async {
    await _questionsRef.doc(question.id).set({
      'text': question.text,
      'senderId': question.senderId,
      'receiverId': question.receiverId,
      'timestamp': Timestamp.fromDate(question.timestamp),
      'isAnonymous': question.isAnonymous,
    });
  }

  // Stream of questions for a specific user (Receiver)
  Stream<List<app_models.Question>> getQuestionsForUser(String userId) {
    return _questionsRef
        .where('receiverId', isEqualTo: userId)
        .orderBy('timestamp', descending: true)
        .snapshots()
        .map((snapshot) {
      return snapshot.docs.map((doc) {
        final data = doc.data() as Map<String, dynamic>;
        return app_models.Question(
          id: doc.id,
          text: data['text'] ?? '',
          senderId: data['senderId'] ?? 'anonymous',
          receiverId: data['receiverId'] ?? '',
          timestamp: (data['timestamp'] as Timestamp).toDate(),
          isAnonymous: data['isAnonymous'] ?? true,
        );
      }).toList();
    });
  }
}
