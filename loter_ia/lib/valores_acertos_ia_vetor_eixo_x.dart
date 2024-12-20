// ignore_for_file: depend_on_referenced_packages, prefer_typing_uninitialized_variables

//import 'package:cloud_firestore/cloud_firestore.dart'; // Import necessário para Firestore

List<int> valoresAcertosIAVetorEixoX() {
  /// MODIFY CODE ONLY BELOW THIS LINE

  List<Map<String, dynamic>> officialResults = []; // Dados do Firestore (megasenacsv)
  List<Map<String, dynamic>> generatedResults = []; // Dados do Firestore (resultadosreduzidoscsv)

  // Função para carregar dados de uma coleção
  Future<void> fetchFirestoreData() async {
    try {
      // Busca dados da coleção "megasenacsv"
      QuerySnapshot querySnapshot = await FirebaseFirestore.instance
          .collection('megasenacsv')
          .get();
      officialResults = querySnapshot.docs.map((doc) {
        return {
          'Date': doc['Date'],
          'Bola1': int.tryParse(doc['Bola1'] ?? '0') ?? 0,
          'Bola2': int.tryParse(doc['Bola2'] ?? '0') ?? 0,
          'Bola3': int.tryParse(doc['Bola3'] ?? '0') ?? 0,
          'Bola4': int.tryParse(doc['Bola4'] ?? '0') ?? 0,
          'Bola5': int.tryParse(doc['Bola5'] ?? '0') ?? 0,
          'Bola6': int.tryParse(doc['Bola6'] ?? '0') ?? 0,
        };
      }).toList();

      // Busca dados da coleção "resultadosreduzidoscsv"
      QuerySnapshot resultSnapshot = await FirebaseFirestore.instance
          .collection('resultadosreduzidoscsv')
          .get();
      generatedResults = resultSnapshot.docs.map((doc) {
        return {
          'Bola1': int.tryParse(doc['Bola1'] ?? '0') ?? 0,
          'Bola2': int.tryParse(doc['Bola2'] ?? '0') ?? 0,
          'Bola3': int.tryParse(doc['Bola3'] ?? '0') ?? 0,
          'Bola4': int.tryParse(doc['Bola4'] ?? '0') ?? 0,
          'Bola5': int.tryParse(doc['Bola5'] ?? '0') ?? 0,
          'Bola6': int.tryParse(doc['Bola6'] ?? '0') ?? 0,
        };
      }).toList();
    } catch (e) {
      print('Erro ao buscar dados do Firestore: $e');
    }
  }

  // Calcular acertos
  List<int> calculateHits(
    List<Map<String, dynamic>> officialResults,
    List<Map<String, dynamic>> generatedResults,
  ) {
    List<int> totalHitsPerGame = [];

    for (var generated in generatedResults) {
      Set<int> generatedSet = {
        generated['Bola1'],
        generated['Bola2'],
        generated['Bola3'],
        generated['Bola4'],
        generated['Bola5'],
        generated['Bola6'],
      };

      int hitsForGame = 0;
      for (var official in officialResults) {
        Set<int> officialSet = {
          official['Bola1'],
          official['Bola2'],
          official['Bola3'],
          official['Bola4'],
          official['Bola5'],
          official['Bola6'],
        };

        hitsForGame += generatedSet.intersection(officialSet).length;
      }

      totalHitsPerGame.add(hitsForGame);
    }

    return totalHitsPerGame;
  }

  // Executa busca e cálculos
  fetchFirestoreData().then((_) {
    final hits = calculateHits(officialResults, generatedResults);
    return hits;
  });

  return [];
  /// MODIFY CODE ONLY ABOVE THIS LINE
}

class FirebaseFirestore {
  static var instance;
}

class QuerySnapshot {
  var docs;
}
