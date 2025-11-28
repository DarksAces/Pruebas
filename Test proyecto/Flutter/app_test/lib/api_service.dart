// lib/api_service.dart

import 'package:cloud_firestore/cloud_firestore.dart';

// Modelo de datos para el nuevo sitio a subir
class NewStopData {
  final String title;
  final String author;
  final String? comment; 
  final double lat;
  final double lng;

  NewStopData({
    required this.title,
    required this.author,
    this.comment, 
    required this.lat,
    required this.lng,
  });
}

// Lógica de comunicación con Firebase
class ApiService {
  final _firestore = FirebaseFirestore.instance;

  // 1. Subida de nuevos sitios (Metadatos)
  Future<bool> uploadNewStop(NewStopData stopData) async {
    try {
      print('🚀 INICIANDO SUBIDA DE METADATOS...');
      print('📍 Ubicación: ${stopData.lat}, ${stopData.lng}');
      print('📝 Título: ${stopData.title}');
      
      final imageUrl = 'https://images.unsplash.com/photo-1579547621876-13e68dfd04c1?auto=format&fit=crop&q=80&w=200&h=200';
      print('🔗 Usando URL por defecto: $imageUrl');

      print('💾 Guardando en Firestore...');
      final dataToUpload = {
        'title': stopData.title,
        'author': stopData.author.isEmpty ? 'Anónimo' : stopData.author,
        'type': stopData.comment ?? 'Sin comentario',
        'lat': stopData.lat,
        'lng': stopData.lng,
        'imageUrl': imageUrl, 
        'createdAt': FieldValue.serverTimestamp(),
      };
      
      final docRef = await _firestore.collection('sitios').add(dataToUpload);

      print('✅ Documento creado con ID: ${docRef.id}');
      print('🎉 SUBIDA COMPLETADA EXITOSAMENTE');
      return true;

    } on FirebaseException catch (e) {
      print('═══════════════════════════════════════');
      print('🚨 ERROR DE FIREBASE');
      print('═══════════════════════════════════════');
      print('Código: ${e.code}');
      print('Mensaje: ${e.message}');
      print('Plugin: ${e.plugin}');
      if (e.stackTrace != null) print('Stack: ${e.stackTrace}');
      print('═══════════════════════════════════════');
      
      if (e.code == 'permission-denied') {
        print('💡 SOLUCIÓN: Configura las reglas de Firestore (permitir lectura/escritura).');
      } else if (e.code == 'network-request-failed') {
        print('💡 SOLUCIÓN: Verifica tu conexión a internet');
      }
      
      return false;
      
    } catch (e, stackTrace) {
      print('═══════════════════════════════════════');
      print('🚨 ERROR GENÉRICO');
      print('═══════════════════════════════════════');
      print('Excepción: $e');
      print('Stack trace: $stackTrace');
      print('═══════════════════════════════════════');
      return false;
    }
  }

  // 2. Añadir Comentario a un Sitio
  Future<bool> addComment({
    required String stopId,
    required String nickname,
    required String text,
  }) async {
    if (text.trim().isEmpty) return false;

    try {
      await _firestore
          .collection('sitios')
          .doc(stopId)
          .collection('comments')
          .add({ 
        'nickname': nickname,
        'text': text,
        'timestamp': FieldValue.serverTimestamp(),
      });
      print('✅ Comentario añadido a sitio $stopId por $nickname');
      return true;
    } catch (e) {
      print('❌ Error al añadir comentario: $e');
      return false;
    }
  }
  
  // 3. checkAndRegisterNickname ELIMINADO
}