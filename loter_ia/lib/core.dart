// ignore_for_file: avoid_function_literals_in_foreach_calls

import 'package:loter_ia/fetch_sheet_data.dart';

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

List<List<int>> bolasPremiadas = [
  [7, 25, 8, 23, 36, 46, 54],
  [6, 20, 7, 39, 47, 51, 52],
  [7, 49, 8, 23, 36, 46, 54],
  [4, 59, 5, 20, 47, 53, 56],
  [4, 1, 7, 42, 47, 48, 51],
  [7, 35, 8, 35, 43, 53, 58],
  [8, 41, 9, 14, 32, 53, 59],
  [6, 8, 8, 38, 50, 53, 59],
  [8, 55, 9, 11, 48, 53, 60],
  [1, 49, 8, 30, 36, 47, 53],
  [3, 45, 9, 35, 37, 41, 49],
  [5, 41, 6, 34, 46, 53, 55],
  [1, 36, 2, 24, 40, 51, 59],
  [5, 36, 6, 34, 46, 53, 55],
  [6, 30, 7, 39, 47, 51, 52],
  [7, 18, 8, 23, 36, 46, 54],
  [8, 26, 9, 11, 48, 53, 60],
  [5, 32, 7, 37, 43, 53, 54],
  [5, 9, 8, 18, 42, 52, 59],
  [3, 47, 9, 20, 36, 53, 54],
  [7, 9, 9, 39, 43, 44, 60],
  [6, 12, 7, 39, 47, 51, 52],
  [4, 27, 6, 39, 46, 54, 58],
  [4, 9, 7, 42, 47, 48, 51],
  [5, 34, 6, 34, 46, 53, 55],
  [6, 39, 8, 38, 50, 53, 59],
  [1, 22, 2, 24, 40, 51, 59],
  [8, 20, 9, 39, 44, 49, 58],
  [8, 18, 9, 39, 44, 49, 58],
  [4, 47, 8, 27, 44, 54, 59],
  [8, 3, 9, 25, 41, 57, 60],
  [4, 26, 7, 42, 47, 48, 51],
  [7, 48, 8, 23, 36, 46, 54],
  [8, 34, 9, 25, 41, 57, 60],
  [3, 36, 6, 29, 36, 47, 59],
  [5, 20, 7, 37, 43, 53, 54],
  [4, 33, 7, 42, 47, 48, 51],
  [5, 44, 7, 37, 43, 53, 54],
  [4, 20, 7, 42, 47, 48, 51],
  [7, 59, 9, 30, 44, 51, 60],
  [4, 23, 8, 27, 44, 54, 59],
  [7, 22, 8, 35, 43, 53, 58],
  [7, 13, 8, 23, 36, 46, 54],
  [8, 16, 9, 39, 44, 49, 58],
  [4, 60, 7, 42, 47, 48, 51],
  [2, 3, 3, 17, 49, 50, 59],
  [8, 59, 9, 39, 44, 49, 58],
  [1, 37, 2, 24, 40, 51, 59],
  [1, 42, 5, 12, 47, 52, 59],
  [2, 25, 4, 29, 52, 56, 60],
  [4, 48, 7, 42, 47, 48, 51],
  [5, 1, 7, 37, 43, 53, 54],
  [2, 39, 8, 27, 32, 49, 56],
  [8, 49, 9, 39, 44, 49, 58],
  [8, 52, 9, 39, 44, 49, 58],
  [4, 50, 8, 27, 44, 54, 59],
  [4, 58, 7, 42, 47, 48, 51],
  [7, 6, 8, 23, 36, 46, 54],
  [3, 53, 8, 36, 40, 51, 53],
  [4, 40, 8, 27, 44, 54, 59],
  [1, 59, 2, 24, 40, 51, 59],
  [3, 32, 9, 20, 36, 53, 54],
  [1, 50, 8, 34, 41, 53, 58],
  [1, 49, 8, 30, 36, 47, 53],
];

void main() async {
  // Dados fictícios de resultados oficiais
  List<Map<String, dynamic>> officialResults = await resultadosOficiais();
  //{Date: 2024-12-01, Bola1: 6, Bola2: 20, Bola3: 7, Bola4: 39, Bola5: 47, Bola6: 6}
  //  [
  //   {'Date': '2024-12-01', 'Bola1': 6, 'Bola2': 20, 'Bola3': 7, 'Bola4': 39, 'Bola5': 47, 'Bola6': 8},
  //   {'Date': '2024-12-02', 'Bola1': 7, 'Bola2': 8, 'Bola3': 9, 'Bola4': 10, 'Bola5': 11, 'Bola6': 12},
  // ];
  print(officialResults.last);

  // Dados de resultados gerados
  List<Map<String, dynamic>> generatedResults = bolasPremiadas.map((bolas) {
  return {
       'Bola1': bolas[0],
       'Bola2': bolas[1],
       'Bola3': bolas[2],
       'Bola4': bolas[3],
       'Bola5': bolas[4],
       'Bola6': bolas[5],
     };
  }).toList();
  print(generatedResults.last);

  // Testando calculateHitsWithPrizes
  List<Map<String, dynamic>> hitsWithPrizes = calculateHitsWithPrizes(officialResults, generatedResults);
  print('ACERTOS COM PREMIO:');
  hitsWithPrizes.forEach((result) => (result['Hits'] > 0 && result['Category'] > 0) ? print(result) : print('.'));

  // // Testando calculateFrequency
   List<Map<String, dynamic>> frequency = calculateFrequency(hitsWithPrizes);
   print('\nFrequency:');
   frequency.forEach((freq) => freq['Hits4'] > 0 ? print(freq) : null);

  print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n');
}
