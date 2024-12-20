// ignore_for_file: prefer_typing_uninitialized_variables

import 'package:csv/csv.dart';
import 'package:loter_ia/fetch_sheet_data.dart';

const PRIZE_4 = 1070.51;
const PRIZE_5 = 42563.82;
const PRIZE_6 = 16000000.00;

List<Map<String, dynamic>> calculateHitsWithPrizes(
  List<Map<String, dynamic>> officialResults,
  List<Map<String, dynamic>> generatedResults,
) {
  List<Map<String, dynamic>> resultData = [];

  for (var generated in generatedResults) {
    Set<int> generatedSet = {
      generated['Bola1'],
      generated['Bola2'],
      generated['Bola3'],
      generated['Bola4'],
      generated['Bola5'],
      generated['Bola6'],
    };

    for (var official in officialResults) {
      Set<int> officialSet = {
        official['Bola1'],
        official['Bola2'],
        official['Bola3'],
        official['Bola4'],
        official['Bola5'],
        official['Bola6'],
      };

      int hits = generatedSet.intersection(officialSet).length;

      // Atualiza a frequência para 4, 5 ou 6 acertos
      resultData.add({
        'Date': official['Date'], // Data do sorteio
        'Hits': hits, // Número de acertos
        'Category': hits >= 4 ? hits : 0, // Categoriza apenas 4, 5 ou 6
      });
    }
  }

  return resultData;
}

List<Map<String, dynamic>> calculateFrequency(
  List<Map<String, dynamic>> results,
) {
  Map<String, Map<int, int>> frequencyMap = {};

  for (var result in results) {
    String date = result['Date'];
    int category = result['Category'];

    if (category > 0) {
      if (!frequencyMap.containsKey(date)) {
        frequencyMap[date] = {4: 0, 5: 0, 6: 0};
      }
      frequencyMap[date]![category] = frequencyMap[date]![category]! + 1;
    }
  }

  // Converte para uma lista de mapas para usar no gráfico
  List<Map<String, dynamic>> consolidatedData = [];
  frequencyMap.forEach((date, counts) {
    consolidatedData.add({
      'Date': date,
      'Hits4': counts[4],
      'Hits5': counts[5],
      'Hits6': counts[6],
    });
  });

  return consolidatedData;
}

List<Map<String, dynamic>> calculateEachTotalPrize(
  List<Map<String, dynamic>> frequency,
) {
  List<Map<String, dynamic>> prizes = [];

  for (var freq in frequency) {
    double totalPrize4 = (freq['Hits4'] ?? 0) * PRIZE_4;
    double totalPrize5 = (freq['Hits5'] ?? 0) * PRIZE_5;
    double totalPrize6 = (freq['Hits6'] ?? 0) * PRIZE_6;

    prizes.add({
      'Date': freq['Date'],
      'TotalPrize4': totalPrize4,
      'TotalPrize5': totalPrize5,
      'TotalPrize6': totalPrize6,
      'TotalPrize': totalPrize4 + totalPrize5 + totalPrize6,
    });
  }

  return prizes;
}

// Função para buscar dados do Google Sheets
Future<List<Map<String, dynamic>>> fetchSheetData(String sheetUrl) async {
  try {
    // Faz o request para a URL pública do CSV
    var http;
    final response = await http.get(Uri.parse(sheetUrl));

    if (response.statusCode == 200) {
      // Converte o conteúdo CSV em uma lista de mapas
      final csvData = const CsvToListConverter().convert(response.body);

      // Assumindo que a primeira linha contém os cabeçalhos
      final headers = csvData.first.cast<String>();
      final rows = csvData.skip(1);

      // Converte as linhas em um formato de lista de mapas
      return rows.map((row) {
        return Map<String, dynamic>.fromIterables(
          headers,
          row,
        );
      }).toList();
    } else {
      throw Exception('Erro ao acessar a planilha: ${response.statusCode}');
    }
  } catch (e) {
    throw Exception('Erro ao buscar dados do Google Sheets: $e');
  }
}

Future<List<Map<String, dynamic>>> main() async {
   
   List<Map<String, dynamic>> officialResults = await resultadosOficiais();

  // Dados fictícios de resultados gerados
  List<Map<String, dynamic>> generatedResults = [
    {'Bola1': 1, 'Bola2': 2, 'Bola3': 3, 'Bola4': 13, 'Bola5': 14, 'Bola6': 15},
    {'Bola1': 7, 'Bola2': 8, 'Bola3': 9, 'Bola4': 4, 'Bola5': 5, 'Bola6': 6},
    {'Bola1': 7, 'Bola2': 8, 'Bola3': 9, 'Bola4': 10, 'Bola5': 5, 'Bola6': 6},
    {'Bola1': 7, 'Bola2': 8, 'Bola3': 9, 'Bola4': 10, 'Bola5': 11, 'Bola6': 6},
  ];

  // Testando calculateHitsWithPrizes
  List<Map<String, dynamic>> hitsWithPrizes =
      calculateHitsWithPrizes(officialResults, generatedResults);
  //print('Hits With Prizes:');
  // for (var result in hitsWithPrizes) {
  //   //print(result);
  // }

  // Testando calculateFrequency
  List<Map<String, dynamic>> frequency = calculateFrequency(hitsWithPrizes);
  //print('\nFrequency:');
  // for (var freq in frequency) {
  //   // print(freq);
  // }

  return officialResults; // [officialResults, generatedResults, hitsWithPrizes, frequency];
}

