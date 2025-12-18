import 'package:flutter/material.dart';
import 'package:flutter_card_swiper/flutter_card_swiper.dart';
import '../models/models.dart';
import '../widgets/user_card.dart';
import '../services/database_service.dart';
import 'package:firebase_auth/firebase_auth.dart'; // Added

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(
          'Discover',
          style: Theme.of(context).textTheme.headlineSmall?.copyWith(
            fontWeight: FontWeight.bold,
          ),
        ),
        centerTitle: false,
        actions: [
          IconButton(
            icon: const Icon(Icons.tune),
            onPressed: () {},
          ),
        ],
      ),
      body: SafeArea(
        child: StreamBuilder<List<User>>(
          stream: DatabaseService().getUsers(),
          builder: (context, snapshot) {
            if (snapshot.connectionState == ConnectionState.waiting) {
              return const Center(child: CircularProgressIndicator());
            }

            if (!snapshot.hasData || snapshot.data!.isEmpty) {
              return const Center(child: Text('No users found.'));
            }

            // Realistically filter out current user and blocked users
            // For now, we show all users
            final users = snapshot.data!;

            return Column(
              children: [
                Expanded(
                  child: CardSwiper(
                    cardsCount: users.length,
                    numberOfCardsDisplayed: users.length > 3 ? 3 : users.length,
                    backCardOffset: const Offset(0, 40),
                    padding: const EdgeInsets.all(24.0),
                    cardBuilder: (context, index, percentThresholdX, percentThresholdY) {
                      return UserCard(user: users[index]);
                    },
                    onSwipe: (previousIndex, currentIndex, direction) {
                      final currentUser = FirebaseAuth.instance.currentUser;
                      if (currentUser == null) return false;

                      final targetUser = users[previousIndex];
                      final isLike = direction == CardSwiperDirection.right;

                      DatabaseService().recordSwipe(currentUser.uid, targetUser.id, isLike).then((isMatch) {
                        if (isMatch) {
                           ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text('It\'s a Match with ${targetUser.name}!'),
                              backgroundColor: Colors.pink,
                              duration: const Duration(seconds: 2),
                            ),
                          );
                        }
                      });

                      if (direction == CardSwiperDirection.right) {
                         // Optional: immediate feedback before server response
                      }
                      return true;
                    },
                  ),
                ),
                // Action Buttons
                Padding(
                  padding: const EdgeInsets.only(bottom: 24.0),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      _ActionButton(
                        icon: Icons.close,
                        color: Colors.red,
                        onPressed: () {
                          // Controller would be used here to trigger swipe programmatically
                        },
                      ),
                      _ActionButton(
                        icon: Icons.star,
                        color: Colors.blue,
                        isSmall: true,
                        onPressed: () {},
                      ),
                      _ActionButton(
                        icon: Icons.favorite,
                        color: Colors.green,
                        onPressed: () {},
                      ),
                    ],
                  ),
                ),
              ],
            );
          },
        ),
      ),
    );
  }
}

class _ActionButton extends StatelessWidget {
  final IconData icon;
  final Color color;
  final VoidCallback onPressed;
  final bool isSmall;

  const _ActionButton({
    required this.icon,
    required this.color,
    required this.onPressed,
    this.isSmall = false,
  });

  @override
  Widget build(BuildContext context) {
    final size = isSmall ? 50.0 : 60.0;
    
    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(
        shape: BoxShape.circle,
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.1),
            blurRadius: 10,
            spreadRadius: 2,
          ),
        ],
      ),
      child: IconButton(
        icon: Icon(icon, color: color),
        onPressed: onPressed,
      ),
    );
  }
}
