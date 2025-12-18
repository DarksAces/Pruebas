import 'package:flutter/material.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../models/models.dart' as app_models; // Alias to avoid conflict
import '../services/database_service.dart';
import '../widgets/user_card.dart'; // We might re-use this or just show avatars

class MatchesScreen extends StatelessWidget {
  const MatchesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final currentUser = FirebaseAuth.instance.currentUser;

    if (currentUser == null) {
      return const Center(child: Text('Please log in to see matches'));
    }

    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Matches',
          style: Theme.of(context).textTheme.headlineSmall?.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
      ),
      body: StreamBuilder<List<app_models.User>>(
        stream: DatabaseService().getMatches(currentUser.uid),
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
             // In a real app we'd handle this better, but for now we expect errors if API is disabled
             return Center(child: Text('Error: ${snapshot.error}'));
          }

          if (!snapshot.hasData || snapshot.data!.isEmpty) {
            return const Center(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  Icon(Icons.heart_broken, size: 80, color: Colors.grey),
                  SizedBox(height: 16),
                  Text('No matches yet. Keep swiping!', style: TextStyle(color: Colors.grey)),
                ],
              ),
            );
          }

          final matches = snapshot.data!;

          return ListView.separated(
            padding: const EdgeInsets.all(16),
            itemCount: matches.length,
            separatorBuilder: (ctx, i) => const Divider(),
            itemBuilder: (context, index) {
              final user = matches[index];
              return ListTile(
                leading: CircleAvatar(
                  radius: 30,
                  backgroundImage: NetworkImage(user.imageUrl),
                  onBackgroundImageError: (_, __) => const Icon(Icons.person),
                ),
                title: Text(
                   user.name,
                   style: const TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
                ),
                subtitle: const Text('You matched! Say hi!'), // Placeholder for last message
                trailing: const Icon(Icons.chat_bubble_outline, color: Colors.deepPurple),
                onTap: () {
                   ScaffoldMessenger.of(context).showSnackBar(
                     SnackBar(content: Text('Chat with ${user.name} coming soon!')),
                   );
                },
              );
            },
          );
        },
      ),
    );
  }
}
