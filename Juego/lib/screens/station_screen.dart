import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:google_fonts/google_fonts.dart';
import '../models/player_state.dart';
import '../services/localization.dart';
import '../services/world_manager.dart';
import '../services/iap_service.dart';

class StationScreen extends StatelessWidget {
  const StationScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final player = context.watch<PlayerState>();
    final loc = context.watch<Localization>();

    return DefaultTabController(
      length: 4,
      child: Container(
        color: Colors.grey[900],
        height: 600,
        child: Column(
          children: [
            Padding(
              padding: const EdgeInsets.all(16.0),
              child: Column(
                children: [
                  Text(loc.get('station_title'), style: GoogleFonts.orbitron(color: Colors.white, fontSize: 24, fontWeight: FontWeight.bold)),
                  Text('${loc.get('credits')}: \$${player.credits.ceil()}', style: const TextStyle(color: Colors.greenAccent, fontSize: 18)),
                ],
              ),
            ),
            TabBar(
              labelColor: Colors.amber,
              unselectedLabelColor: Colors.white54,
              indicatorColor: Colors.amber,
              tabs: [
                Tab(icon: const Icon(Icons.shopping_bag), text: loc.get('tab_consumables')),
                Tab(icon: const Icon(Icons.security), text: loc.get('tab_equipment')),
                Tab(icon: const Icon(Icons.monetization_on), text: loc.get('tab_bank')),
                const Tab(icon: Icon(Icons.public), text: 'Travel'),
              ],
            ),
            Expanded(
              child: TabBarView(
                children: [
                  // Consumables Tab
                  ListView(
                    padding: const EdgeInsets.all(16),
                    children: [
                      _buildShopItem(context, player, 'Nano-Potion', 'Heal 50 HP', 30),
                      _buildShopItem(context, player, loc.get('item_mega_potion'), loc.get('desc_mega_potion'), 100),
                      _buildShopItem(context, player, loc.get('item_energy_cell'), loc.get('desc_energy_cell'), 50),
                      _buildShopItem(context, player, loc.get('item_nano_elixir'), loc.get('desc_nano_elixir'), 80),
                      _buildShopItem(context, player, loc.get('item_strength_potion'), loc.get('desc_strength_potion'), 150),
                      _buildShopItem(context, player, loc.get('item_iron_skin_potion'), loc.get('desc_iron_skin_potion'), 150),
                      _buildShopItem(context, player, loc.get('item_luck_charm'), loc.get('desc_luck_charm'), 200),
                      _buildShopItem(context, player, loc.get('item_overcharge'), loc.get('desc_overcharge'), 150),
                      _buildShopItem(context, player, loc.get('item_hyper_shield'), loc.get('desc_hyper_shield'), 120),
                      _buildShopItem(context, player, 'Phoenix Chip', 'Revive on death', 500),
                    ],
                  ),
                  
                  // Equipment & Services Tab
                  ListView(
                    padding: const EdgeInsets.all(16),
                    children: [
                      ListTile(
                        leading: const Icon(Icons.local_hospital, color: Colors.redAccent),
                        title: Text(loc.get('full_heal'), style: const TextStyle(color: Colors.white)),
                        subtitle: Text(loc.get('restore_hp'), style: const TextStyle(color: Colors.white70)),
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
                      const Divider(color: Colors.white24),
                      _buildShopItem(context, player, loc.get('item_titanium_plating'), loc.get('desc_titanium_plating'), 1000),
                      _buildShopItem(context, player, loc.get('item_neural_link'), loc.get('desc_neural_link'), 1000),
                      const Divider(color: Colors.white24),
                      _buildWeaponItem(context, player, loc.get('item_pulse_rifle'), 30, 800),
                      _buildWeaponItem(context, player, loc.get('weapon_excalibur'), 60, 1500), // Medieval
                      _buildWeaponItem(context, player, loc.get('weapon_bone_club'), 70, 1800), // Prehistoric
                      _buildWeaponItem(context, player, loc.get('weapon_laser_katana'), 90, 2500), // Future
                      _buildWeaponItem(context, player, loc.get('weapon_magic_wand'), 100, 3000), // Fantasy
                      _buildWeaponItem(context, player, loc.get('item_neutron_cannon'), 80, 3500),
                      _buildWeaponItem(context, player, loc.get('weapon_void_cannon'), 50, 2000),
                      _buildWeaponItem(context, player, loc.get('item_singularity'), 150, 10000),
                    ],
                  ),

                  // Bank (Real Money) Tab
                  ListView(
                    padding: const EdgeInsets.all(16),
                    children: [
                      _buildIAPItem(context, player, loc.get('pack_small'), 'small_credit_pack', 1000, 0.99),
                      _buildIAPItem(context, player, loc.get('pack_medium'), 'medium_credit_pack', 5000, 3.99),
                      _buildIAPItem(context, player, loc.get('pack_large'), 'large_credit_pack', 15000, 9.99),
                    ],
                  ),

                  // Travel Tab
                  ListView.builder(
                    padding: const EdgeInsets.all(16),
                    itemCount: WorldManager.worlds.length,
                    itemBuilder: (ctx, index) {
                      final world = WorldManager.worlds[index];
                      final isUnlocked = player.unlockedWorlds.contains(world.id);
                      final isCurrent = player.currentWorldId == world.id;

                      return Card(
                        color: isUnlocked 
                            ? (isCurrent ? Colors.blue[900] : Colors.grey[850]) 
                            : Colors.black54,
                        margin: const EdgeInsets.only(bottom: 12),
                        child: ListTile(
                          leading: Icon(
                            isUnlocked ? Icons.public : Icons.lock, 
                            color: isUnlocked ? Colors.cyanAccent : Colors.grey
                          ),
                          title: Text(
                            loc.get(world.name), 
                            style: TextStyle(
                              color: isUnlocked ? Colors.white : Colors.grey, 
                              fontWeight: FontWeight.bold
                            )
                          ),
                          subtitle: isUnlocked 
                              ? Text(loc.get(world.description), style: const TextStyle(color: Colors.white70))
                              : Text(
                                  loc.get('unlock_reach_floor').replaceFirst('%s', _getPreviousWorldName(player, world.id, loc)),
                                  style: const TextStyle(color: Colors.redAccent, fontStyle: FontStyle.italic)
                                ),
                          trailing: isCurrent
                              ? const Icon(Icons.location_on, color: Colors.blueAccent)
                              : isUnlocked
                                  ? ElevatedButton(
                                      style: ElevatedButton.styleFrom(backgroundColor: Colors.amber[800]),
                                      onPressed: () {
                                        player.travelTo(world.id);
                                        ScaffoldMessenger.of(context).showSnackBar(
                                          SnackBar(content: Text('${loc.get('travel')} -> ${loc.get(world.name)}!')),
                                        );
                                      },
                                      child: Text(loc.get('travel')),
                                    )
                                  : Icon(Icons.lock_outline, color: Colors.white24),
                        ),
                      );
                    },
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  String _getPreviousWorldName(PlayerState player, String currentWorldId, Localization loc) {
     // Naive implementation: find previous index in master list.
     // In reality, we should ask WorldManager or PlayerState for the "unlock parent".
     // For now, based on strict order:
     final order = [
      'kingdom_valor',
      'jurassica',
      'neon_tokyo',
      'mystic_woods',
      'void_nexus'
    ];
    int index = order.indexOf(currentWorldId);
    if (index > 0) {
      String prevId = order[index - 1];
      // Get name from localized ID
      // We don't have direct access to World object here easily without searching WorldManager again, which is fine.
      final prevWorld = WorldManager.getWorld(prevId);
      return loc.get(prevWorld.name);
    }
    return "Unknown";
  }


  Widget _buildShopItem(BuildContext context, PlayerState player, String itemId, String desc, double cost) {
    final canAfford = player.credits >= cost;
    return ListTile(
      leading: const Icon(Icons.shopping_bag, color: Colors.orangeAccent),
      title: Text(itemId, style: const TextStyle(color: Colors.white)),
      subtitle: Text(desc, style: const TextStyle(color: Colors.white70)),
      trailing: ElevatedButton(
        style: ElevatedButton.styleFrom(backgroundColor: canAfford ? Colors.blue[900] : Colors.grey),
        onPressed: canAfford
            ? () {
                player.gainCredits(-cost);
                player.addItem(itemId);
                ScaffoldMessenger.of(context).showSnackBar(
                  SnackBar(content: Text('Bought $itemId!')),
                );
              }
            : null,
        child: Text('\$${cost.ceil()}', style: const TextStyle(color: Colors.white)),
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
  Widget _buildIAPItem(BuildContext context, PlayerState player, String name, String productId, double credits, double price) {
    final iapService = context.watch<IAPService>();

    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 8.0),
      child: ElevatedButton(
        style: ElevatedButton.styleFrom(
          backgroundColor: Colors.amber[800],
          padding: const EdgeInsets.symmetric(horizontal: 32, vertical: 16),
        ),
        onPressed: () {
          if (productId.isNotEmpty) {
            iapService.buyProduct(productId);
          }
        },
        child: Text("$name (+${credits.ceil()} Credits) - \$$price", style: const TextStyle(fontSize: 16, color: Colors.white)),
      ),
    );
  }
}
