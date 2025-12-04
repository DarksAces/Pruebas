import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../models/player_state.dart';

class UpgradeScreen extends StatelessWidget {
  const UpgradeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final state = context.watch<PlayerState>();

    return Container(
      padding: const EdgeInsets.all(16),
      height: 400,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Ship Upgrades', style: TextStyle(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
          const SizedBox(height: 20),
          
          _buildUpgradeTile(
            context,
            title: 'Laser Damage',
            subtitle: 'Current: ${state.clickDamage.toStringAsFixed(1)} dmg',
            cost: state.upgradeCostClick,
            onTap: () => context.read<PlayerState>().buyClickUpgrade(),
            icon: Icons.flash_on,
            color: Colors.redAccent,
          ),
          
          const SizedBox(height: 10),

          _buildUpgradeTile(
            context,
            title: 'Auto-Turrets',
            subtitle: 'Current: ${state.autoDamage.toStringAsFixed(1)} DPS',
            cost: state.upgradeCostAuto,
            onTap: () => context.read<PlayerState>().buyAutoUpgrade(),
            icon: Icons.settings_input_antenna,
            color: Colors.blueAccent,
          ),

          const Spacer(),
          
          Center(
            child: ElevatedButton(
              style: ElevatedButton.styleFrom(backgroundColor: Colors.purple[900]),
              onPressed: () {
                showDialog(
                  context: context,
                  builder: (ctx) => AlertDialog(
                    title: const Text('Prestige?'),
                    content: const Text('Reset all progress to gain Dark Matter? (Requires Stage 10)'),
                    actions: [
                      TextButton(onPressed: () => Navigator.pop(ctx), child: const Text('Cancel')),
                      TextButton(
                        onPressed: () {
                          context.read<PlayerState>().prestige();
                          Navigator.pop(ctx);
                          Navigator.pop(context);
                        }, 
                        child: const Text('PRESTIGE', style: TextStyle(color: Colors.red))
                      ),
                    ],
                  )
                );
              },
              child: const Text('PRESTIGE (Reset)', style: TextStyle(color: Colors.white)),
            ),
          )
        ],
      ),
    );
  }

  Widget _buildUpgradeTile(BuildContext context, {
    required String title, 
    required String subtitle, 
    required double cost, 
    required VoidCallback onTap,
    required IconData icon,
    required Color color,
  }) {
    final canAfford = context.read<PlayerState>().credits >= cost;
    
    return Card(
      color: Colors.grey[800],
      child: ListTile(
        leading: Icon(icon, color: color, size: 30),
        title: Text(title, style: const TextStyle(color: Colors.white, fontWeight: FontWeight.bold)),
        subtitle: Text(subtitle, style: const TextStyle(color: Colors.white70)),
        trailing: ElevatedButton(
          style: ElevatedButton.styleFrom(
            backgroundColor: canAfford ? Colors.green : Colors.grey,
          ),
          onPressed: canAfford ? onTap : null,
          child: Text('\$${cost.toStringAsFixed(0)}', style: const TextStyle(color: Colors.white)),
        ),
      ),
    );
  }
}
