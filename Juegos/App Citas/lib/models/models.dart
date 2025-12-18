
class User {
  final String id;
  final String name;
  final int age;
  final String bio;
  final String imageUrl;
  final List<String> photos;

  User({
    required this.id,
    required this.name,
    required this.age,
    required this.bio,
    required this.imageUrl,
    required this.photos,
  });

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'name': name,
      'age': age,
      'bio': bio,
      'imageUrl': imageUrl,
      'photos': photos,
    };
  }

  factory User.fromMap(Map<String, dynamic> map, String id) {
    return User(
      id: id,
      name: map['name'] ?? '',
      age: map['age'] ?? 0,
      bio: map['bio'] ?? '',
      imageUrl: map['imageUrl'] ?? '',
      photos: List<String>.from(map['photos'] ?? []),
    );
  }
}

class Question {
  final String id;
  final String text;
  final String senderId; // Can be 'anonymous'
  final String receiverId;
  final DateTime timestamp;
  final bool isAnonymous;

  Question({
    required this.id,
    required this.text,
    required this.senderId,
    required this.receiverId,
    required this.timestamp,
    required this.isAnonymous,
  });

  Map<String, dynamic> toMap() {
    return {
      'text': text,
      'senderId': senderId,
      'receiverId': receiverId,
      'timestamp': timestamp.millisecondsSinceEpoch,
      'isAnonymous': isAnonymous,
    };
  }

  factory Question.fromMap(Map<String, dynamic> map, String id) {
    return Question(
      id: id,
      text: map['text'] ?? '',
      senderId: map['senderId'] ?? 'anonymous',
      receiverId: map['receiverId'] ?? '',
      timestamp: DateTime.fromMillisecondsSinceEpoch(map['timestamp'] ?? 0),
      isAnonymous: map['isAnonymous'] ?? true,
    );
  }
}

// MOCK DATA REMOVED OR KEPT FOR REFERENCE IF NEEDED, BUT CLEANER TO REMOVE IF WE HAVE REAL BACKEND
// Keeping it simpler by removing the mock data lists entirely as we will use Firestore.

