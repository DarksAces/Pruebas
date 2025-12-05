
import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import '../models/models.dart' as app_models;

import 'package:firebase_auth/firebase_auth.dart';
import '../services/database_service.dart';

class QuestionsScreen extends StatelessWidget {
  const QuestionsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return const Center(child: Text('Please login'));

    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Questions',
          style: Theme.of(context).textTheme.headlineSmall?.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
        actions: [
          IconButton(
            icon: const FaIcon(FontAwesomeIcons.paperPlane),
            onPressed: () {
               // Demo: Send a question to self
               final q = app_models.Question(
                 id: DateTime.now().millisecondsSinceEpoch.toString(),
                 text: 'How are you finding the app?',
                 senderId: 'anonymous',
                 receiverId: user.uid,
                 timestamp: DateTime.now(),
                 isAnonymous: true,
               );
               DatabaseService().saveQuestion(q);
               ScaffoldMessenger.of(context).showSnackBar(
                  const SnackBar(content: Text('Sent demo question to self')),
                );
            },
          ),
        ],
      ),
      body: StreamBuilder<List<app_models.Question>>(
        stream: DatabaseService().getQuestionsForUser(user.uid),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }
          
          if (!snapshot.hasData || snapshot.data!.isEmpty) {
             return const Center(child: Text('No questions yet.'));
          }

          final questions = snapshot.data!;

          return ListView.builder(
            padding: const EdgeInsets.all(16),
            itemCount: questions.length,
            itemBuilder: (context, index) {
              return _QuestionCard(question: questions[index]);
            },
          );
        },
      ),
    );
  }
}

class _QuestionCard extends StatelessWidget {
  final app_models.Question question;

  const _QuestionCard({required this.question});

  @override
  Widget build(BuildContext context) {
    // Generate a random-ish color based on ID or index if available,
    // for now we cycle or pick a nice gradient.
    final bool isAnonymous = question.isAnonymous;

    return Container(
      margin: const EdgeInsets.only(bottom: 16),
      decoration: BoxDecoration(
        color: Theme.of(context).cardColor,
        borderRadius: BorderRadius.circular(16),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.05),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.stretch,
        children: [
          // Header (Gradient bar)
          Container(
            height: 60,
            decoration: BoxDecoration(
              borderRadius: const BorderRadius.vertical(top: Radius.circular(16)),
              gradient: LinearGradient(
                colors: isAnonymous
                    ? [const Color(0xFF8E2DE2), const Color(0xFF4A00E0)] // Deep Purple for Anonymous
                    : [const Color(0xFFf12711), const Color(0xFFf5af19)], // Orange for Named
              ),
            ),
            padding: const EdgeInsets.symmetric(horizontal: 16),
            child: Row(
              children: [
                CircleAvatar(
                  backgroundColor: Colors.white.withOpacity(0.2),
                   child: FaIcon(
                    isAnonymous ? FontAwesomeIcons.userSecret : FontAwesomeIcons.user,
                    color: Colors.white,
                    size: 18,
                   ),
                ),
                const SizedBox(width: 12),
                Text(
                  isAnonymous ? 'Anonymous' : 'User ${question.senderId}', // Ideally fetch user name
                  style: const TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.bold,
                    fontSize: 16,
                  ),
                ),
                const Spacer(),
                Text(
                  '${question.timestamp.minute}m ago', // Simplified time
                  style: TextStyle(
                    color: Colors.white.withOpacity(0.8),
                    fontSize: 12,
                  ),
                ),
              ],
            ),
          ),
          
          // Question Text
          Padding(
            padding: const EdgeInsets.all(20),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  question.text,
                  style: const TextStyle(
                    fontSize: 18,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(height: 16),
                
                // Action Buttons
                Row(
                  mainAxisAlignment: MainAxisAlignment.end,
                  children: [
                    TextButton.icon(
                      onPressed: () {},
                      icon: const Icon(Icons.delete_outline, color: Colors.grey),
                      label: const Text('Delete', style: TextStyle(color: Colors.grey)),
                    ),
                    const SizedBox(width: 8),
                    ElevatedButton.icon(
                      onPressed: () {},
                      icon: const Icon(Icons.reply, size: 18),
                      label: const Text('Reply'),
                      style: ElevatedButton.styleFrom(
                        padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
