# ingesta_bot_ultra.py

import firebase_admin
from firebase_admin import credentials, firestore
import time
import random
import datetime
import json
from io import StringIO

# --- CONFIGURACIÓN DE CREDENCIALES DIRECTAS ---
# 🚨 ESTE DICCIONARIO CONTIENE TUS CREDENCIALES PRIVADAS. MANTÉNELO SEGURO.
SERVICE_ACCOUNT_INFO = {
  "type": "service_account",
  "project_id": "jovi-45c79",
  "private_key_id": "32d9c5fa65801a2cc7ccebfa35d26552961f0645",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQCmpJUt29xI0gIu\nIO/I1fS6R66xeFgVofCS+zUVVYsErFEne0mXu7qXu2eu2gA7GnlgZ3te8EaO/brB\nMilrRaYu43b+9YPbyUblED2TyLdfG2QCESONynlT35XKOZZin7nfraqmJ8qVviiS\nU24+ODffzwKciSK+Er4YjEXJckeLMwgaEExaxMFuxMWNL5VAYNrXhNN+tpO/OTfx\nAmR10bKtmDApH/MtEXCrTUa65VXLein1TmHJjws5Wf9JgeFzhrXJ2G2Q26YraTSZ\nDDM6yjCarKkA5M2sQLdKJn5zbIR/F5cnvVtCGaPd8gjl1QX7zvsaztXZHTkHRc9b\nkPx9zJO1AgMBAAECgf8e+U3BIwc5gc9l7jlOMHaMfpu54OR+djCBIVrR3FSP9Hd2\ndIlOlVYusxFShAgG9E9whnYn71aDaCXjmFnv1mz3yiUUFA5Y4SXhmGMu/4prOGwe\nS5E63vzY2iC9YHbTXgeZIRksSQ5z8XnDuOjaJ8OQQKn7mSxxUoqC2uUdzF//6e8O\n78Q1ug3XtD0vaJocm0cVEou5mYYpGoMPjfdTI3FFQ+nsdhvcGFbsOa9BhxIaSSRa\njerggB/EZIxxRWZqCks6MmL1f48mYc1/sxFGon0SSNhT3Z3xPWJp3QUSTZnt+wQz\nBnLiiTBAQwneQY+7cA3OX6QQJP2QIjfOwer/SCkCgYEA54zx4bS8P2ss5yQLHE0A\n7OlBbrscwxFQ760uuYKA9Xr0VAv1wref2WPSJk2oX45f8TbhNs+1UaPzWavB5jCI\nJihbay2OLptyKEIDaSd6wflrNmX0xskW9Ynk7FR5OyNi9JUAH5KAou5t8tF6bVuS\nIeINpKdhTwX561q9pU3tUhkCgYEAuD0dkN2p1XrOkzzcFxqaXBocJb3i5iTtLrju\n3yiNnsCKqG9vDuY5X5bvkJyESHrZPdJxFrjVry1L118OZBJydRWoVWN5TmosNOIB\ntSLPlBPnyBUYrOhqzQgAeOqNCHE73+yhiUiQFydgdG1VJXdxjtS3nSK/qTmRN0Lc\n4wruGf0CgYEA0yEMCF6Q606hMd0GmHaKKnsBY6MPNbqbTv9dRF9/kNXc5KnHHBXslf7TxoM2zHJ4fuwobJ712IwivxfChE6qRgi0WsS+CTdJ3vVaQM5zu1zeakqK55rB6X8jkm3v4IGCoDsgUql1y5qV/DsPY5mEZIrHH+RS8Qgk+nnRxGGKzDkCgYAIYsfAu0YqsF9Mtl1yM8TI4mtbkGwOe6nMEaDVyXvAuRTWm9PbQsFjx3P6ChW/UtAmjziUhy86vP4RvILkLS7Gg4jY8iEoX47JjWv0ebQnEkzff45S+HU8Bdw3pL1sn/LQu22S2Rmt5B3wzrUscmZZ0PbWkSlWI4enk0SIlQvHZQKBgCrYi/3kxA7QC3vevcqXUJC8\n0DGZdKH0bOTQHYBQzx+QrUp7UjaV/vmfsSxid5m/gyRmhEdb8gkI2qmGHYb29mH5\nsIxcqLnayYkUO++putoVR00m8hN5RNdWW12OnqiP3SPa016TfHXmRaoEPA5jppUN\nYpIfwb+JrwQLRxLgkp5x\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-fbsvc@jovi-45c79.iam.gserviceaccount.com",
  "client_id": "116528390919363869339",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-fbsvc%40jovi-45c79.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# Atribución solicitada
ADMIN_BOT_AUTHOR = "DarkAce" 
ADMIN_BOT_ID = "DarkAceID" 

# --- DATOS GLOBALES PARA INGESTAR (35+ EJEMPLOS VARIADOS) ---
SITIOS_FAMOSOS_PARA_INGESTAR = [
  {"title": "Estatua de la Libertad", "lat": 40.6892, "lng": -74.0445, "type": "Monumento", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Torre Eiffel", "lat": 48.8584, "lng": 2.2945, "type": "Monumento", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Gran Muralla China", "lat": 40.4319, "lng": 116.5704, "type": "Historia", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Coliseo Romano", "lat": 41.8902, "lng": 12.4922, "type": "Historia", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Ópera de Sídney", "lat": -33.8568, "lng": 151.2153, "type": "Arquitectura", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Taj Mahal", "lat": 27.1751, "lng": 78.0421, "type": "Patrimonio", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Cristo Redentor", "lat": -22.9519, "lng": -43.2105, "type": "Monumento", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Pirámides de Giza", "lat": 29.9792, "lng": 31.1342, "type": "Historia", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Machu Picchu", "lat": -13.1631, "lng": -72.5450, "type": "Patrimonio", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Catedral de San Basilio", "lat": 55.7525, "lng": 37.6231, "type": "Arquitectura", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "La Mona Lisa (Louvre)", "lat": 48.8606, "lng": 2.3376, "type": "Arte Clásico", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Guernica (Reina Sofía)", "lat": 40.4087, "lng": -3.6946, "type": "Arte Moderno", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "El Beso (Klimt)", "lat": 48.1923, "lng": 16.3811, "type": "Arte Clásico", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Noche Estrellada (MoMA)", "lat": 40.7614, "lng": -73.9776, "type": "Arte Moderno", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Joven de la Perla", "lat": 52.0792, "lng": 4.3168, "type": "Arte Clásico", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Hallstatt", "lat": 47.5573, "lng": 13.6534, "type": "Pueblo Pintoresco", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Shirakawa-go", "lat": 36.2575, "lng": 136.8851, "type": "Pueblo Tradicional", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Chefchaouen", "lat": 35.1718, "lng": -5.2635, "type": "Ciudad Azul", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Matera (Sassi)", "lat": 40.6689, "lng": 16.6083, "type": "Pueblo Histórico", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Sintra (Pena)", "lat": 38.7876, "lng": -9.3904, "type": "Pueblo Real", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Giethoorn", "lat": 52.7303, "lng": 6.0772, "type": "Pueblo sin Carreteras", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Lago Bled", "lat": 46.3687, "lng": 14.1090, "type": "Naturaleza", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Cataratas del Niágara", "lat": 43.0828, "lng": -79.0742, "type": "Naturaleza", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Gran Cañón", "lat": 36.1069, "lng": -112.1129, "type": "Naturaleza", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Monte Fuji", "lat": 35.3606, "lng": 138.7292, "type": "Montaña", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Copacabana", "lat": -22.9715, "lng": -43.1866, "type": "Playa", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Salar de Uyuni", "lat": -20.2038, "lng": -67.6200, "type": "Naturaleza", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Fiordo Geiranger", "lat": 62.1158, "lng": 7.0864, "type": "Fiordo", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Angkor Wat", "lat": 13.4125, "lng": 103.8670, "type": "Templo", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Chichén Itzá", "lat": 20.6843, "lng": -88.5678, "type": "Pirámide", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Alhambra", "lat": 37.1760, "lng": -3.5888, "type": "Patrimonio", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Isla de Pascua (Moáis)", "lat": -27.1167, "lng": -109.3667, "type": "Misterio", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Rothenburg ob der Tauber", "lat": 49.3783, "lng": 10.1780, "type": "Pueblo Medieval", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Colmar", "lat": 48.0795, "lng": 7.3585, "type": "Pueblo", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Bruges", "lat": 51.2093, "lng": 3.2247, "type": "Histórico", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Kotor", "lat": 42.4247, "lng": 18.7712, "type": "Fortaleza", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Cesky Krumlov", "lat": 48.8119, "lng": 14.3152, "type": "Medieval", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Mostar", "lat": 43.3373, "lng": 17.8150, "type": "Puente Histórico", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Tallin Casco Antiguo", "lat": 59.4370, "lng": 24.7536, "type": "Ciudad Medieval", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Riga Old Town", "lat": 56.9496, "lng": 24.1052, "type": "Centro Histórico", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Vilna Old Town", "lat": 54.6872, "lng": 25.2797, "type": "Centro Histórico", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Lucerna", "lat": 47.0502, "lng": 8.3093, "type": "Ciudad", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Bruarfoss", "lat": 64.2645, "lng": -20.3053, "type": "Cascada", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Skogafoss", "lat": 63.5321, "lng": -19.5118, "type": "Cascada", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Seljalandsfoss", "lat": 63.6156, "lng": -19.9928, "type": "Cascada", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Gullfoss", "lat": 64.3261, "lng": -20.1200, "type": "Cascada", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Kirkjufell", "lat": 64.9249, "lng": -23.3080, "type": "Montaña", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Playa Navagio", "lat": 37.8590, "lng": 20.6246, "type": "Playa", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Santorini Oia", "lat": 36.4618, "lng": 25.3753, "type": "Isla", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Mykonos", "lat": 37.4467, "lng": 25.3289, "type": "Isla", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Ibiza Dalt Vila", "lat": 38.9089, "lng": 1.4327, "type": "Fortaleza", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Menorca (Cala Macarella)", "lat": 39.9403, "lng": 3.9331, "type": "Playa", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Mallorca (Cala S'Almunia)", "lat": 39.3102, "lng": 3.1490, "type": "Playa", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Tenerife Teide", "lat": 28.2724, "lng": -16.6425, "type": "Montaña", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Gran Canaria Roque Nublo", "lat": 27.9508, "lng": -15.6047, "type": "Roca", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Big Ben", "lat": 51.5007, "lng": -0.1246, "type": "Monumento", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Acrópolis de Atenas", "lat": 37.9715, "lng": 23.7267, "type": "Historia", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Sagrada Familia", "lat": 41.4036, "lng": 2.1744, "type": "Arquitectura", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Torre de Pisa", "lat": 43.7230, "lng": 10.3966, "type": "Monumento", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Puente Golden Gate", "lat": 37.8199, "lng": -122.4783, "type": "Arquitectura", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Petra", "lat": 30.3285, "lng": 35.4444, "type": "Historia", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Stonehenge", "lat": 51.1789, "lng": -1.8262, "type": "Misterio", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Burj Khalifa", "lat": 25.1972, "lng": 55.2744, "type": "Arquitectura", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Mezquita Azul", "lat": 41.0054, "lng": 28.9768, "type": "Patrimonio", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Templo Kinkaku-ji", "lat": 35.0394, "lng": 135.7292, "type": "Templo", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Palacio de Versalles", "lat": 48.8049, "lng": 2.1204, "type": "Patrimonio", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Catedral de Notre-Dame", "lat": 48.8530, "lng": 2.3499, "type": "Patrimonio", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Neuschwanstein", "lat": 47.5576, "lng": 10.7498, "type": "Castillo", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Monte Rushmore", "lat": 43.8791, "lng": -103.4591, "type": "Monumento", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Tikal", "lat": 17.2221, "lng": -89.6236, "type": "Historia", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Victoria Falls", "lat": -17.9243, "lng": 25.8572, "type": "Naturaleza", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Cataratas del Iguazú", "lat": -25.6953, "lng": -54.4367, "type": "Naturaleza", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Parque Nacional Yellowstone", "lat": 44.4280, "lng": -110.5885, "type": "Naturaleza", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Banff National Park", "lat": 51.4968, "lng": -115.9281, "type": "Naturaleza", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Torres del Paine", "lat": -51.2500, "lng": -72.9667, "type": "Naturaleza", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Fiordos Noruegos", "lat": 61.0000, "lng": 7.0000, "type": "Fiordo", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Lago Moraine", "lat": 51.3322, "lng": -116.1847, "type": "Naturaleza", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Cinque Terre", "lat": 44.1267, "lng": 9.7229, "type": "Pueblo Costero", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Positano", "lat": 40.6280, "lng": 14.4850, "type": "Pueblo Costero", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Ronda", "lat": 36.7429, "lng": -5.1607, "type": "Pueblo", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Mont Saint-Michel", "lat": 48.6361, "lng": -1.5115, "type": "Monasterio", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Meteora", "lat": 39.7217, "lng": 21.6306, "type": "Monasterios", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Capadocia", "lat": 38.6431, "lng": 34.8289, "type": "Naturaleza", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Palacio de la Alhambra", "lat": 37.1760, "lng": -3.5881, "type": "Palacio", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Acantilados de Moher", "lat": 52.9719, "lng": -9.4265, "type": "Naturaleza", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Parque Güell", "lat": 41.4145, "lng": 2.1527, "type": "Arquitectura", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Dubrovnik Murallas", "lat": 42.6407, "lng": 18.1083, "type": "Ciudad Fortificada", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Bagan", "lat": 21.1717, "lng": 94.8586, "type": "Templos", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Borobudur", "lat": -7.6079, "lng": 110.2038, "type": "Templo", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Bahía de Ha Long", "lat": 20.9101, "lng": 107.1839, "type": "Naturaleza", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Playa Maya Bay", "lat": 7.6805, "lng": 98.7677, "type": "Playa", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Parque Nacional Plitvice", "lat": 44.8654, "lng": 15.5820, "type": "Naturaleza", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Preikestolen", "lat": 58.9864, "lng": 6.1904, "type": "Acantilado", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Trolltunga", "lat": 60.1241, "lng": 6.7400, "type": "Formación Rocosa", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Lofoten", "lat": 68.2181, "lng": 13.5336, "type": "Archipiélago", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Jokulsarlon", "lat": 64.0484, "lng": -16.1797, "type": "Laguna Glaciar", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Parque Nacional Vatnajökull", "lat": 64.4147, "lng": -16.8090, "type": "Glaciar", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Landmannalaugar", "lat": 63.9962, "lng": -19.0634, "type": "Montañas", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Milford Sound", "lat": -44.6719, "lng": 167.9260, "type": "Fiordo", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Monte Cook", "lat": -43.5950, "lng": 170.1418, "type": "Montaña", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Hobbiton", "lat": -37.8721, "lng": 175.6831, "type": "Cinematográfico", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Lago Tekapo", "lat": -44.0045, "lng": 170.4771, "type": "Lago", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Uluru", "lat": -25.3444, "lng": 131.0369, "type": "Formación Rocosa", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Gran Barrera de Coral", "lat": -18.2871, "lng": 147.6992, "type": "Arrecife", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Twelve Apostles", "lat": -38.6656, "lng": 143.1048, "type": "Formaciones Rocosas", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Whitehaven Beach", "lat": -20.2817, "lng": 149.0392, "type": "Playa", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Bondi Beach", "lat": -33.8908, "lng": 151.2743, "type": "Playa", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Desierto de Atacama", "lat": -23.5000, "lng": -69.2500, "type": "Desierto", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Glaciar Perito Moreno", "lat": -50.4950, "lng": -73.1375, "type": "Glaciar", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Viñedos de Mendoza", "lat": -33.1301, "lng": -68.8781, "type": "Viñedos", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Valle de la Luna", "lat": -22.9167, "lng": -68.2667, "type": "Paisaje Lunar", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Cartagena de Indias", "lat": 10.3910, "lng": -75.4794, "type": "Ciudad Colonial", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Caño Cristales", "lat": 2.1850, "lng": -73.7850, "type": "Río", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Parque Tayrona", "lat": 11.3000, "lng": -74.0500, "type": "Parque Nacional", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Islas Galápagos", "lat": -0.9538, "lng": -90.9656, "type": "Archipiélago", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Centro Histórico de Quito", "lat": -0.2201, "lng": -78.5122, "type": "Ciudad Colonial", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Amazonas", "lat": -3.4653, "lng": -62.2159, "type": "Selva", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Pan de Azúcar", "lat": -22.9068, "lng": -43.1729, "type": "Montaña", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Ipanema", "lat": -22.9838, "lng": -43.2047, "type": "Playa", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Fernando de Noronha", "lat": -3.8549, "lng": -32.4228, "type": "Isla", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Lençóis Maranhenses", "lat": -2.4856, "lng": -43.1289, "type": "Dunas", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Palacio Imperial de Tokio", "lat": 35.6852, "lng": 139.7528, "type": "Palacio", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"},
  {"title": "Fushimi Inari", "lat": 34.9671, "lng": 135.7727, "type": "Santuario", "imageUrl": "https://firebasestorage.googleapis.com/v0/b/jovi-45c79.firebasestorage.app/o/stop_photos%2F1764172336632-Centro_de_Estudios_Monlau.jpg?alt=media&token=383b771d-38b5-4804-a492-436b74014fbd"} 
  ]

# Inicializar Firebase
try:
    # 💡 CAMBIO CLAVE: Cargar las credenciales del diccionario
    cred = credentials.Certificate(SERVICE_ACCOUNT_INFO) 
    firebase_admin.initialize_app(cred)
    db = firestore.client()
    print("✅ Conexión a Firebase Admin establecida directamente.")
except Exception as e:
    print(f"❌ Error al inicializar Firebase Admin: {e}")
    print("VERIFICA que el DICCIONARIO SERVICE_ACCOUNT_INFO esté COMPLETO y CORRECTO.")
    exit()

def is_duplicated(lat, lng):
    """Verifica si ya existe un sitio en Firestore con coordenadas similares."""
    epsilon = 0.00001
    
    query = db.collection('sitios') \
        .where('lat', '>', lat - epsilon) \
        .where('lat', '<', lat + epsilon) \
        .where('lng', '>', lng - epsilon) \
        .where('lng', '<', lng + epsilon) \
        .limit(1)

    return query.get()

def upload_site_to_firestore(site_data):
    """Añade un documento a la colección 'sitios' con un ID generado automáticamente."""
    
    # 1. Verificar duplicados
    existing_sites = is_duplicated(site_data['lat'], site_data['lng'])
    if existing_sites:
        print(f"⚠️ SITIO IGNORADO (DUPLICADO): '{site_data['title']}' ya existe.")
        return False

    # 2. El ID es generado automáticamente con .document()
    doc_ref = db.collection('sitios').document() 
    
    data = {
        'title': site_data['title'],
        'lat': site_data['lat'],
        'lng': site_data['lng'],
        'type': site_data['type'],
        'imageUrl': site_data['imageUrl'],
        
        # Atribución solicitada
        'author': ADMIN_BOT_AUTHOR, 
        'authorId': ADMIN_BOT_ID, 
        
        'createdAt': firestore.SERVER_TIMESTAMP,
    }

    try:
        doc_ref.set(data)
        print(f"✅ SITIO SUBIDO: '{site_data['title']}' - ID automático: {doc_ref.id}")
        return True
    except Exception as e:
        print(f"❌ ERROR al subir {site_data['title']}: {e}")
        return False


# --- INGESTA PRINCIPAL ---
if __name__ == "__main__":
    print(f"\n--- Iniciando Ingestión Ultra Masiva de {len(SITIOS_FAMOSOS_PARA_INGESTAR)} Sitios ---")
    
    successful_uploads = 0
    for site in SITIOS_FAMOSOS_PARA_INGESTAR:
        if upload_site_to_firestore(site):
            successful_uploads += 1
        
        # Pausa para evitar sobrecargar Firestore
        time.sleep(random.uniform(0.1, 0.5))
    
    print(f"\n--- Proceso Finalizado. {successful_uploads} sitios subidos por {ADMIN_BOT_AUTHOR}. ---")