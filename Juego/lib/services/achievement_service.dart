import 'package:flutter/foundation.dart';
import 'package:shared_preferences/shared_preferences.dart';

class Achievement {
  final String id;
  final String title;
  final String description;
  final bool hidden;
  bool isUnlocked;

  Achievement({
    required this.id,
    required this.title,
    required this.description,
    this.hidden = false,
    this.isUnlocked = false,
  });
}

class AchievementService extends ChangeNotifier {
  final List<Achievement> _achievements = [
    Achievement(
        id: 'first_blood',
        title: 'First Blood',
        description: 'Defeat your first enemy.'),
    Achievement(
        id: 'novice_hunter',
        title: 'Novice Hunter',
        description: 'Reach Level 5.'),
    Achievement(
        id: 'big_spender',
        title: 'Big Spender',
        description: 'Accumulate 1000 credits.'),
    Achievement(
        id: 'boss_killer',
        title: 'Boss Killer',
        description: 'Defeat a Boss monster.',
        hidden: true),
    Achievement(
        id: 'survivor',
        title: 'Survivor',
        description: 'Win a fight with less than 10 HP remaining.',
        hidden: true),
  ];

  List<Achievement> get achievements => _achievements;

  // New achievements unlocked in the current session (for UI notification)
  final List<Achievement> _recentlyUnlocked = []; 
  List<Achievement> get recentlyUnlocked => List.unmodifiable(_recentlyUnlocked);

  void clearRecentlyUnlocked() {
    _recentlyUnlocked.clear();
    // No notify needed usually, unless UI binds directly to this
  }

  void unlock(String id) {
    final index = _achievements.indexWhere((a) => a.id == id);
    if (index != -1 && !_achievements[index].isUnlocked) {
      _achievements[index].isUnlocked = true;
      _recentlyUnlocked.add(_achievements[index]);
      _save();
      notifyListeners();
    }
  }

  // Persistence
  Future<void> load() async {
    final prefs = await SharedPreferences.getInstance();
    final unlockedIds = prefs.getStringList('unlockedAchievements') ?? [];
    
    for (var id in unlockedIds) {
      final index = _achievements.indexWhere((a) => a.id == id);
      if (index != -1) {
        _achievements[index].isUnlocked = true;
      }
    }
    notifyListeners();
  }

  Future<void> _save() async {
    final prefs = await SharedPreferences.getInstance();
    final unlockedIds = _achievements
        .where((a) => a.isUnlocked)
        .map((a) => a.id)
        .toList();
    await prefs.setStringList('unlockedAchievements', unlockedIds);
  }
}
