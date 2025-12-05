
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
}

// MOCK DATA
final List<User> mockUsers = [
  User(
    id: '1',
    name: 'Sofia',
    age: 23,
    bio: 'Architecture student & Coffee lover ☕',
    imageUrl: 'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
    photos: [
      'https://images.unsplash.com/photo-1494790108377-be9c29b29330?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
      'https://images.unsplash.com/photo-1534528741775-53994a69daeb?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
    ],
  ),
  User(
    id: '2',
    name: 'Mateo',
    age: 26,
    bio: 'Photographer and Traveler 📸. Always looking for the next adventure.',
    imageUrl: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
    photos: [
      'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
    ],
  ),
  User(
    id: '3',
    name: 'Valentina',
    age: 24,
    bio: 'Art & Design. Lets create something beautiful.',
    imageUrl: 'https://images.unsplash.com/photo-1517841905240-472988babdf9?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
    photos: [
      'https://images.unsplash.com/photo-1517841905240-472988babdf9?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
    ],
  ),
   User(
    id: '4',
    name: 'Lucas',
    age: 25,
    bio: 'Musician 🎸. I play guitar and sing.',
    imageUrl: 'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
    photos: [
       'https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?ixlib=rb-1.2.1&auto=format&fit=crop&w=500&q=60',
    ],
  ),
];

final List<Question> mockQuestions = [
  Question(
    id: 'q1',
    text: 'What is your favorite travel destination?',
    senderId: 'anonymous',
    receiverId: 'currentUser',
    timestamp: DateTime.now().subtract(const Duration(minutes: 5)),
    isAnonymous: true,
  ),
  Question(
    id: 'q2',
    text: 'Do you believe in love at first sight?',
    senderId: '2',
    receiverId: 'currentUser',
    timestamp: DateTime.now().subtract(const Duration(hours: 2)),
    isAnonymous: false,
  ),
    Question(
    id: 'q3',
    text: 'Whats your hidden talent?',
    senderId: 'anonymous',
    receiverId: 'currentUser',
    timestamp: DateTime.now().subtract(const Duration(days: 1)),
    isAnonymous: true,
  ),
];
