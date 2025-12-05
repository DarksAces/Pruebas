
import 'package:flutter/material.dart';
import 'package:font_awesome_flutter/font_awesome_flutter.dart';
import 'package:firebase_auth/firebase_auth.dart';
import '../services/auth_service.dart';

class ProfileScreen extends StatelessWidget {
  const ProfileScreen({super.key});

  @override
  Widget build(BuildContext context) {
    // Get current user from Firebase
    final user = FirebaseAuth.instance.currentUser;
    if (user == null) return const Center(child: Text('Please Login'));

    return Scaffold(
      body: SingleChildScrollView(
        child: Column(
          children: [
            // Header with Photo
            Stack(
              clipBehavior: Clip.none,
              alignment: Alignment.bottomCenter,
              children: [
                // Background Cover
                Container(
                  height: 200,
                  width: double.infinity,
                  decoration: BoxDecoration(
                    color: Theme.of(context).primaryColor.withOpacity(0.1),
                    image: const DecorationImage(
                      image: NetworkImage('https://images.unsplash.com/photo-1579546929518-9e396f3cc809?ixlib=rb-1.2.1&auto=format&fit=crop&w=1000&q=80'),
                      fit: BoxFit.cover,
                    ),
                  ),
                ),
                // Profile Image
                Positioned(
                  bottom: -60,
                  child: Container(
                    decoration: BoxDecoration(
                      shape: BoxShape.circle,
                      border: Border.all(color: Theme.of(context).scaffoldBackgroundColor, width: 5),
                    ),
                    child: CircleAvatar(
                      radius: 60,
                      backgroundImage: NetworkImage(user.photoURL ?? 'https://via.placeholder.com/150'),
                    ),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 70),
            
            // Name & Bio
            Text(
              user.displayName ?? 'User',
              style: Theme.of(context).textTheme.headlineSmall?.copyWith(
                fontWeight: FontWeight.bold,
              ),
            ),
             const SizedBox(height: 8),
            Text(
              user.email ?? 'No Email',
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodyMedium?.copyWith(
                color: Colors.grey,
              ),
            ),
            const SizedBox(height: 24),

            // Stats
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: [
                _StatItem(label: 'Matches', value: '124'),
                _StatItem(label: 'Questions', value: '58'),
                _StatItem(label: 'Likes', value: '2.4k'),
              ],
            ),
            
            const SizedBox(height: 32),
            const Divider(),
            
            // Menu Items
            _ProfileMenuItem(
              icon: Icons.settings,
              title: 'Settings',
              onTap: () {},
            ),
             _ProfileMenuItem(
              icon: Icons.edit,
              title: 'Edit Profile',
              onTap: () {},
            ),
             _ProfileMenuItem(
              icon: FontAwesomeIcons.crown,
              title: 'Get Premium',
              onTap: () {},
              isHighlight: true,
            ),
             _ProfileMenuItem(
              icon: Icons.logout,
              title: 'Logout',
              onTap: () async {
                 await AuthService().signOut();
              },
              isDestructive: true,
            ),
          ],
        ),
      ),
    );
  }
}

class _StatItem extends StatelessWidget {
  final String label;
  final String value;

  const _StatItem({required this.label, required this.value});

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        Text(
          value,
          style: const TextStyle(
            fontSize: 22,
            fontWeight: FontWeight.bold,
          ),
        ),
        Text(
          label,
          style: const TextStyle(
            color: Colors.grey,
          ),
        ),
      ],
    );
  }
}

class _ProfileMenuItem extends StatelessWidget {
  final IconData icon;
  final String title;
  final VoidCallback onTap;
  final bool isDestructive;
  final bool isHighlight;

  const _ProfileMenuItem({
    required this.icon,
    required this.title,
    required this.onTap,
    this.isDestructive = false,
    this.isHighlight = false,
  });

  @override
  Widget build(BuildContext context) {
    Color iconColor = Theme.of(context).iconTheme.color ?? Colors.black;
    Color textColor = Theme.of(context).textTheme.bodyLarge?.color ?? Colors.black;

    if (isDestructive) {
      iconColor = Colors.red;
      textColor = Colors.red;
    } else if (isHighlight) {
      iconColor = Colors.amber;
      textColor = Colors.amber[800]!;
    }

    return ListTile(
      leading: Icon(icon, color: iconColor),
      title: Text(
        title,
        style: TextStyle(
          color: textColor,
          fontWeight: isHighlight ? FontWeight.bold : FontWeight.normal,
        ),
      ),
      trailing: const Icon(Icons.arrow_forward_ios, size: 16),
      onTap: onTap,
    );
  }
}
