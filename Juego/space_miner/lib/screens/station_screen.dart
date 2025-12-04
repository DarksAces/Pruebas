import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/player_state.dart';

class StationScreen extends StatelessWidget {
  const StationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final player = context.watch<PlayerState>();

    return Container(
      padding: const EdgeInsets.all(16),
      color: Colors.grey[900],
      height: 500,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Space Station Alpha', style: GoogleFonts.orbitron(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
          const SizedBox(height: 10),
          Text('Credits: \$${player.credits.ceil()}', style: const TextStyle(color: Colors.greenAccent, fontSize: 18)),
          const Divider(color: Colors.white24),
          
          const SizedBox(height: 20),
          const Text('Services', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
          
          ListTile(
            leading: const Icon(Icons.local_hospital, color: Colors.redAccent),
            title: const Text('Full Heal', style: TextStyle(color: Colors.white)),
            subtitle: const Text('Restore 100% HP', style: TextStyle(color: Colors.white70)),
            trailing: ElevatedButton(
              style: ElevatedButton.styleFrom(backgroundColor: Colors.red[900]),
              onPressed: player.credits >= 50 && player.currentHealth < player.maxHealth
                  ? () {
                      player.gainCredits(-50);
                      player.heal(player.maxHealth);
                    }
                  : null,
              child: const Text('\$50', style: TextStyle(color: Colors.white)),
            ),
          ),

          const SizedBox(height: 20),
          const Text('Travel', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
          
          ListTile(
            leading: const Icon(Icons.public, color: Colors.purpleAccent),
            title: const Text('Asteroid Belt', style: TextStyle(color: Colors.white)),
            trailing: player.currentWorldId == 'asteroid_belt' 
                ? const Icon(Icons.location_on, color: Colors.green)
                : ElevatedButton(
                    onPressed: () => player.travelTo('asteroid_belt'),
                    child: const Text('Go'),
                  ),
          ),
          ListTile(
            leading: const Icon(Icons.cloud, color: Colors.blueAccent),
            title: const Text('Nebula Core', style: TextStyle(color: Colors.white)),
            subtitle: const Text('Warning: High Level', style: TextStyle(color: Colors.white70)),
            trailing: player.currentWorldId == 'nebula_core' 
                ? const Icon(Icons.location_on, color: Colors.green)
                : ElevatedButton(
                    onPressed: () => player.travelTo('nebula_core'),
                    child: const Text('Go'),
                  ),
          ),

          const SizedBox(height: 20),
          const Text('Armory', style: TextStyle(color: Colors.white, fontSize: 18, fontWeight: FontWeight.bold)),
          
          _buildWeaponItem(context, player, 'Plasma Rifle', 20, 500),
          _buildWeaponItem(context, player, 'Void Cannon', 50, 2000),
        ],
      ),
    );
  }

  Widget _buildWeaponItem(BuildContext context, PlayerState player, String name, double damage, double cost) {
    final bool alreadyOwned = player.attackDamage >= damage;
    final bool canAfford = player.credits >= cost;

    return ListTile(
      leading: const Icon(Icons.security, color: Colors.blueAccent),
      title: Text(name, style: const TextStyle(color: Colors.white)),
      subtitle: Text('Damage: $damage', style: const TextStyle(color: Colors.white70)),
      trailing: alreadyOwned
          ? const Icon(Icons.check, color: Colors.green)
          : ElevatedButton(
              style: ElevatedButton.styleFrom(backgroundColor: canAfford ? Colors.blue[900] : Colors.grey),
              onPressed: canAfford
                  ? () {
                      player.gainCredits(-cost);
                      player.equipWeapon(name, damage);
                    }
                  : null,
              child: Text('\$${cost.ceil()}', style: const TextStyle(color: Colors.white)),
            ),
    );
  }
}
