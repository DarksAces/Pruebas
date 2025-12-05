import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

class PlayerState extends ChangeNotifier {
  // Stats
  double _currentHealth = 100;
  double _maxHealth = 100;
  double _currentEnergy = 100;
  double _maxEnergy = 100;
  double _shield = 0; // Temporary shield for one turn
  
  int _level = 1;
  double _xp = 0;
  double _xpToNextLevel = 100;
  double _credits = 0;
  
  // Combat Stats
  double _attackDamage = 10;
  double _defense = 0;

  // Inventory / Equipment (Simplified for now)
  String _weaponName = "Rusty Laser Pistol";
  String _armorName = "Flight Suit";

  // Buffs
  bool _nextFightDamageBoost = false;
  bool _nextFightShieldBoost = false;
  bool _nextFightDefenseBoost = false; // Iron Skin
  bool _nextFightLuckBoost = false; // Luck Charm

  // Location & Progression
  String _currentWorldId = "kingdom_valor";
  int _currentFloor = 1;
  final Map<String, int> _maxFloorsReached = {}; // worldId -> maxFloor
  final List<String> _unlockedWorlds = ["kingdom_valor"];

  // Getters
  double get currentHealth => _currentHealth;
  double get maxHealth => _maxHealth;
  double get currentEnergy => _currentEnergy;
  double get maxEnergy => _maxEnergy;
  double get shield => _shield;
  int get level => _level;
  double get xp => _xp;
  double get xpToNextLevel => _xpToNextLevel;
  double get credits => _credits;
  double get attackDamage => _attackDamage;
  String get weaponName => _weaponName;
  String get currentWorldId => _currentWorldId;
  int get currentFloor => _currentFloor;
  List<String> get unlockedWorlds => _unlockedWorlds;
  bool get nextFightDamageBoost => _nextFightDamageBoost;
  bool get nextFightShieldBoost => _nextFightShieldBoost;
  bool get nextFightDefenseBoost => _nextFightDefenseBoost;
  bool get nextFightLuckBoost => _nextFightLuckBoost;

  // Actions
  void enableDamageBoost() {
    _nextFightDamageBoost = true;
    notifyListeners();
  }

  void consumeDamageBoost() {
    _nextFightDamageBoost = false;
    notifyListeners();
  }

  void enableShieldBoost() {
    _nextFightShieldBoost = true;
    notifyListeners();
  }

  void consumeShieldBoost() {
    _nextFightShieldBoost = false;
    notifyListeners();
  }

  void enableDefenseBoost() {
    _nextFightDefenseBoost = true;
    notifyListeners();
  }

  void consumeDefenseBoost() {
    _nextFightDefenseBoost = false;
    notifyListeners();
  }

  void enableLuckBoost() {
    _nextFightLuckBoost = true;
    notifyListeners();
  }

  void consumeLuckBoost() {
    _nextFightLuckBoost = false;
    notifyListeners();
  }

  void takeDamage(double amount) {
    // Shield absorbs damage first
    double damageAfterShield = (amount - _shield).clamp(0, double.infinity);
    _shield = 0; // Shield breaks after being hit (or expires next turn)
    
    // Defense reduction (Iron Skin reduces damage by 50%)
    double defenseMultiplier = _nextFightDefenseBoost ? 0.5 : 1.0;
    
    double actualDamage = ((damageAfterShield - _defense) * defenseMultiplier).clamp(0, double.infinity);
    _currentHealth = (_currentHealth - actualDamage).clamp(0, _maxHealth);
    notifyListeners();
  }

  void useEnergy(double amount) {
    _currentEnergy = (_currentEnergy - amount).clamp(0, _maxEnergy);
    notifyListeners();
  }

  void restoreEnergy(double amount) {
    _currentEnergy = (_currentEnergy + amount).clamp(0, _maxEnergy);
    notifyListeners();
  }

  void addShield(double amount) {
    _shield = amount;
    notifyListeners();
  }

  void clearShield() {
    _shield = 0;
    notifyListeners();
  }

  void heal(double amount) {
    _currentHealth = (_currentHealth + amount).clamp(0, _maxHealth);
    notifyListeners();
  }

  void gainXp(double amount) {
    _xp += amount;
    if (_xp >= _xpToNextLevel) {
      _levelUp();
    }
    notifyListeners();
  }

  void gainCredits(double amount) {
    // Luck Charm doubles credits
    if (_nextFightLuckBoost) {
      amount *= 2;
    }
    _credits += amount;
    notifyListeners();
  }

  void equipWeapon(String name, double damage) {
    _weaponName = name;
    _attackDamage = damage;
    notifyListeners();
  }

  int getMaxFloorForWorld(String worldId) {
    return _maxFloorsReached[worldId] ?? 1;
  }

  void advanceFloor() {
    _currentFloor++;
    
    // Update Max Floor
    int currentMax = _maxFloorsReached[_currentWorldId] ?? 1;
    if (_currentFloor > currentMax) {
      _maxFloorsReached[_currentWorldId] = _currentFloor;
    }

    // Unlock Next World at Floor 100
    if (_currentFloor == 100) {
      _unlockNextWorld();
    }
    
    save();
    notifyListeners();
  }

  void _unlockNextWorld() {
    const worldOrder = [
      'kingdom_valor',
      'jurassica',
      'neon_tokyo',
      'mystic_woods',
      'void_nexus'
    ];
    
    int currentIndex = worldOrder.indexOf(_currentWorldId);
    if (currentIndex != -1 && currentIndex < worldOrder.length - 1) {
      String nextWorld = worldOrder[currentIndex + 1];
      if (!_unlockedWorlds.contains(nextWorld)) {
        _unlockedWorlds.add(nextWorld);
        notifyListeners(); // UI should show toast about unlock
      }
    }
  }

  void travelTo(String worldId) {
    if (_unlockedWorlds.contains(worldId)) {
      _currentWorldId = worldId;
      _currentFloor = 1; // Reset to floor 1 when traveling? Or keep logic?
      // Logic: User can teleport to checkpoint floors, default to 1
      notifyListeners();
    }
  }
  
  void teleportToFloor(int floor) {
    int maxObtained = _maxFloorsReached[_currentWorldId] ?? 1;
    // Allow teleport to milestones (1, 10, 20...) if reached
    // OR simply allow traveling to any reached floor? 
    // Roguelike standard: usually checkpoints. Let's stick to max floor check.
    if (floor <= maxObtained) {
      _currentFloor = floor;
      notifyListeners();
    }
  }

  void _levelUp() {
    _level++;
    _xp -= _xpToNextLevel;
    _xpToNextLevel *= 1.5;
    _maxHealth += 20;
    _currentHealth = _maxHealth; // Full heal on level up
    _maxEnergy += 10;
    _currentEnergy = _maxEnergy;
    _attackDamage += 5;
    notifyListeners();
  }

  void upgradeMaxHealth(double amount) {
    _maxHealth += amount;
    _currentHealth += amount;
    notifyListeners();
  }

  void upgradeMaxEnergy(double amount) {
    _maxEnergy += amount;
    _currentEnergy += amount;
    notifyListeners();
  }

  // Inventory
  final List<String> _inventory = []; // Store item IDs

  List<String> get inventory => _inventory;

  void addItem(String itemId) {
    _inventory.add(itemId);
    notifyListeners();
  }

  void removeItem(String itemId) {
    _inventory.remove(itemId);
    notifyListeners();
  }

  // Persistence
  Future<void> load() async {
    final prefs = await SharedPreferences.getInstance();
    _currentHealth = prefs.getDouble('currentHealth') ?? 100;
    _maxHealth = prefs.getDouble('maxHealth') ?? 100;
    _currentEnergy = prefs.getDouble('currentEnergy') ?? 100;
    _maxEnergy = prefs.getDouble('maxEnergy') ?? 100;
    _level = prefs.getInt('level') ?? 1;
    _xp = prefs.getDouble('xp') ?? 0;
    _xpToNextLevel = prefs.getDouble('xpToNextLevel') ?? 100;
    _credits = prefs.getDouble('credits') ?? 0;
    _attackDamage = prefs.getDouble('attackDamage') ?? 10;
    _currentWorldId = prefs.getString('currentWorldId') ?? "kingdom_valor";
    _currentFloor = prefs.getInt('currentFloor') ?? 1;
    
    _unlockedWorlds.clear();
    _unlockedWorlds.addAll(prefs.getStringList('unlockedWorlds') ?? ["kingdom_valor"]);
    
    // Load map manually from storage if complicated, or simple encoding
    // For simplicity, we just save each world key individually or use JSON
    // Being simple: we reset max floors if we don't implement full map json serialization yet
    // To properly save map:
    // We will assume keys are known or iterate world ids.
    // For now, let's just use "maxFloor_worldId" keys
    _maxFloorsReached.clear();
    for (var worldId in ['kingdom_valor', 'jurassica', 'neon_tokyo', 'mystic_woods', 'void_nexus']) {
       _maxFloorsReached[worldId] = prefs.getInt('maxFloor_$worldId') ?? 1;
    }

    _inventory.clear();
    _inventory.addAll(prefs.getStringList('inventory') ?? []);
    _nextFightDamageBoost = prefs.getBool('nextFightDamageBoost') ?? false;
    _nextFightShieldBoost = prefs.getBool('nextFightShieldBoost') ?? false;
    _nextFightDefenseBoost = prefs.getBool('nextFightDefenseBoost') ?? false;
    _nextFightLuckBoost = prefs.getBool('nextFightLuckBoost') ?? false;
    notifyListeners();
  }

  Future<void> save() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setDouble('currentHealth', _currentHealth);
    await prefs.setDouble('maxHealth', _maxHealth);
    await prefs.setDouble('currentEnergy', _currentEnergy);
    await prefs.setDouble('maxEnergy', _maxEnergy);
    await prefs.setInt('level', _level);
    await prefs.setDouble('xp', _xp);
    await prefs.setDouble('xpToNextLevel', _xpToNextLevel);
    await prefs.setDouble('credits', _credits);
    await prefs.setDouble('attackDamage', _attackDamage);
    await prefs.setString('currentWorldId', _currentWorldId);
    await prefs.setInt('currentFloor', _currentFloor);
    await prefs.setStringList('unlockedWorlds', _unlockedWorlds);
    
    for (var entry in _maxFloorsReached.entries) {
      await prefs.setInt('maxFloor_${entry.key}', entry.value);
    }

    await prefs.setStringList('inventory', _inventory);
    await prefs.setBool('nextFightDamageBoost', _nextFightDamageBoost);
    await prefs.setBool('nextFightShieldBoost', _nextFightShieldBoost);
    await prefs.setBool('nextFightDefenseBoost', _nextFightDefenseBoost);
    await prefs.setBool('nextFightLuckBoost', _nextFightLuckBoost);
  }
}
