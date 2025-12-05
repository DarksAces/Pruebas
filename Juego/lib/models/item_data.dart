class Item {
  final String id;
  final String name;
  final String description;
  final String type; // Weapon, Potion, Utility
  final double value; // Effect value (damage, heal, etc.)
  final int price;

  const Item({
    required this.id,
    required this.name,
    required this.description,
    required this.type,
    required this.value,
    required this.price,
  });
}

class ItemRepository {
  static const List<Item> items = [
    // Consumables
    Item(id: 'nano_potion', name: 'Nano-Potion', description: 'Restores 50 HP', type: 'Potion', value: 50, price: 50),
    Item(id: 'mega_potion', name: 'Mega-Potion', description: 'Restores 150 HP', type: 'Potion', value: 150, price: 120),
    Item(id: 'energy_cell', name: 'Energy Cell', description: 'Restores 50 Energy', type: 'Potion', value: 50, price: 40),
    Item(id: 'nano_elixir', name: 'Nano-Elixir', description: 'Restores 100 Energy', type: 'Potion', value: 100, price: 90),
    
    // Boosts
    Item(id: 'str_potion', name: 'Strength Potion', description: '+50% Dmg (1 Fight)', type: 'Boost', value: 0, price: 80),
    Item(id: 'iron_skin', name: 'Iron Skin', description: '-50% Dmg Taken (1 Fight)', type: 'Boost', value: 0, price: 80),
    Item(id: 'luck_charm', name: 'Luck Charm', description: '2x Credits (1 Fight)', type: 'Boost', value: 0, price: 150),
    
    // Permanent Upgrades (Rare)
    Item(id: 'titanium_plate', name: 'Titanium Plating', description: '+20 Max HP', type: 'Upgrade', value: 20, price: 300),
    Item(id: 'neural_link', name: 'Neural Link', description: '+10 Max Energy', type: 'Upgrade', value: 10, price: 300),
    
    // Weapons (Equippable logic handled separately maybe, or simple replace)
    Item(id: 'plasma_rifle', name: 'Plasma Rifle', description: '30 Dmg', type: 'Weapon', value: 30, price: 500),
    Item(id: 'pulse_cannon', name: 'Pulse Cannon', description: '45 Dmg', type: 'Weapon', value: 45, price: 900),
    Item(id: 'void_blade', name: 'Void Blade', description: '60 Dmg', type: 'Weapon', value: 60, price: 1500),
    Item(id: 'omega_blaster', name: 'Omega Blaster', description: '100 Dmg', type: 'Weapon', value: 100, price: 3000),
  ];

  static Item? getItem(String id) {
    try {
      return items.firstWhere((i) => i.id == id);
    } catch (e) {
      return null;
    }
  }
}
