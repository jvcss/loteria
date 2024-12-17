import 'package:http/http.dart' as http;
import 'package:csv/csv.dart';
import 'dart:convert'; // Necessário para utf8.decode

const PRIZE_4 = 1070.51;
const PRIZE_5 = 42563.82;
const PRIZE_6 = 16000000.00;

// Função para buscar e processar os dados do Google Sheets
Future<List<Map<String, dynamic>>> fetchSheetData(String sheetUrl) async {
  try {
    // Faz o request para a URL pública do CSV
    final response = await http.get(Uri.parse(sheetUrl));

    if (response.statusCode == 200) {
      // Decodifica o corpo da resposta como UTF-8
      final decodedBody = utf8.decode(response.bodyBytes);

      // Converte o conteúdo CSV em uma lista de linhas
      final csvData = const CsvToListConverter(
        eol: '\n',
        fieldDelimiter: '\t',
        convertEmptyTo: ' . ',
      ).convert(decodedBody);

//Concurso
//Data do Sorteio
//Bola1	Bola2	Bola3	Bola4	Bola5	Bola6
//
//Ganhadores 6 acertos
//Cidade / UF
//Rateio 6 acertos
//Ganhadores 5 acertos
//Rateio 5 acertos
//Ganhadores 4 acertos
//Rateio 4 acertos
//Acumulado 6 acertos
//Arrecadação Total
//Estimativa prêmio
//Acumulado Sorteio Especial Mega da Virada
//Observação
      return csvData.map((row) {
        return {
          'Concurso': row[0] ?? '0',
          'Data do Sorteio': row[1] ?? '11/03/1996',
          'Bola1': row[2] ?? '0',
          'Bola2': row[3] ?? '0',
          'Bola3': row[4] ?? '0',
          'Bola4': row[5] ?? '0',
          'Bola5': row[6] ?? '0',
          'Bola6': row[7] ?? '0',
          'Ganhadores 6 acertos': row[8] ?? ' . ',
          'Cidade / UF': row[9] ?? ' . ',
          'Rateio 6 acertos': row[10] ?? '0',
          'Ganhadores 5 acertos': row[11] ?? '0',
          'Rateio 5 acertos': row[12] ?? '0',
          'Ganhadores 4 acertos': row[13] ?? '0',
          'Rateio 4 acertos': row[14] ?? '0',
          'Acumulado 6 acertos': row[15] ?? '0',
          'Arrecadação Total': row[16] ?? '0',
          'Estimativa prêmio': row[17] ?? '0',
          'Acumulado Sorteio Especial Mega da Virada': row[18] ?? '0',
          'Observação': row[19] ?? ' . ',
        };
      }).toList();
    } else {
      throw Exception('Erro ao acessar a planilha: ${response.statusCode}');
    }
  } catch (e) {
    throw Exception('Erro ao buscar dados do Google Sheets: $e');
  }
}

// Calcula acertos e prêmios por categoria
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

      resultData.add({
        'Date': official['Data do Sorteio'],
        'Hits': hits,
        'Category': hits >= 4 ? hits : 0,
      });
    }
  }

  return resultData;
}

// Calcula frequência de acertos por categoria
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

  return frequencyMap.entries.map((entry) {
    return {
      'Date': entry.key,
      'Hits4': entry.value[4] ?? 0,
      'Hits5': entry.value[5] ?? 0,
      'Hits6': entry.value[6] ?? 0,
    };
  }).toList();
}

// Calcula os prêmios totais por categoria
List<Map<String, dynamic>> calculateEachTotalPrize(
    List<Map<String, dynamic>> frequency) {
  return frequency.map((freq) {
    double totalPrize4 = (freq['Hits4'] ?? 0) * PRIZE_4;
    double totalPrize5 = (freq['Hits5'] ?? 0) * PRIZE_5;
    double totalPrize6 = (freq['Hits6'] ?? 0) * PRIZE_6;

    return {
      'Date': freq['Date'],
      'TotalPrize4': totalPrize4,
      'TotalPrize5': totalPrize5,
      'TotalPrize6': totalPrize6,
      'TotalPrize': totalPrize4 + totalPrize5 + totalPrize6,
    };
  }).toList();
}

// Função auxiliar para conversão segura de String para int
int _safeParseInt(dynamic value) {
  if (value == null || value.toString().trim().isEmpty) {
    return 0; // Valor padrão em caso de nulo ou vazio
  }
  try {
    return int.parse(value.toString());
  } catch (e) {
    return 0; // Valor padrão em caso de erro de conversão
  }
}

// Retorna uma lista com os valores de total de ganhos para o eixo Y do gráfico
List<double> getTotalPrizesForChart(
  List<Map<String, dynamic>> officialResults,
  List<Map<String, dynamic>> generatedResults,
) {
  // Utiliza a função `calculateEachTotalPrize` e extrai os valores totais
  List<Map<String, dynamic>> totalPrizes = calculateEachTotalPrize(
    calculateFrequency(
      calculateHitsWithPrizes(officialResults, generatedResults),
    ),
  );

  // Retorna apenas os valores do campo `TotalPrize`
  return totalPrizes
      .map<double>((prize) => prize['TotalPrize'] as double)
      .toList();
}

// Retorna uma lista com as datas para o eixo X do gráfico
List<String> getDatesForChart(
  List<Map<String, dynamic>> officialResults,
  List<Map<String, dynamic>> generatedResults,
) {
  // Utiliza a função `calculateEachTotalPrize` e extrai as datas
  List<Map<String, dynamic>> totalPrizes = calculateEachTotalPrize(
    calculateFrequency(
      calculateHitsWithPrizes(officialResults, generatedResults),
    ),
  );

  // Retorna apenas os valores do campo `Date`
  return totalPrizes.map<String>((prize) => prize['Date'] as String).toList();
}

void main() async {
  const String sheetUrl =
      'https://docs.google.com/spreadsheets/d/17lBepq9eX-O0nrFmNQ14gCKhBUHSsTLCUgDyqJIWOBw/export?format=tsv';
  // Busca os dados da planilha
  List<Map<String, dynamic>> sheetData = await fetchSheetData(sheetUrl);

  print('Dados do Google Sheets:');
  for (var row in sheetData) {
    print(row);
  }

  // Conversão de colunas específicas para int
  List<Map<String, dynamic>> officialResults = sheetData.map((row) {
    return {
      'Data do Sorteio': row['Data do Sorteio'] ?? '11/03/1996',
      'Bola1': _safeParseInt(row['Bola1']),
      'Bola2': _safeParseInt(row['Bola2']),
      'Bola3': _safeParseInt(row['Bola3']),
      'Bola4': _safeParseInt(row['Bola4']),
      'Bola5': _safeParseInt(row['Bola5']),
      'Bola6': _safeParseInt(row['Bola6']),
    };
  }).toList();

  // Dados fictícios de resultados gerados
  List<Map<String, dynamic>> generatedResults = [
    {
      'Bola1': 4,
      'Bola2': 5,
      'Bola3': 30,
      'Bola4': 33,
      'Bola5': 41,
      'Bola6': 52
    },
    {
      'Bola1': 9,
      'Bola2': 37,
      'Bola3': 39,
      'Bola4': 41,
      'Bola5': 43,
      'Bola6': 49
    },
  ];

  // Calcula acertos
  List<Map<String, dynamic>> hitsWithPrizes =
      calculateHitsWithPrizes(officialResults, generatedResults);
  print('\nHits With Prizes:');
  hitsWithPrizes.forEach((result) =>
      (result['Hits'] > 0 && result['Category'] > 0) ? print(result) : null);

  // Calcula frequência
  List<Map<String, dynamic>> frequency = calculateFrequency(hitsWithPrizes);
  print('\nFrequency:');
  frequency.forEach((freq) =>
      (freq['Hits4'] > 0 || freq['Hits5'] > 0 || freq['Hits6'] > 0)
          ? print(freq)
          : null);

  // Calcula prêmios
  List<Map<String, dynamic>> totalPrizes = calculateEachTotalPrize(frequency);
  print('\nTotal Prizes:');
  totalPrizes.forEach((prize) => print(prize));


  // Exemplo de uso dos dados para gráfico
  // Exemplo de uso dos dados para gráfico
  List<double> totalPrizesForChart = getTotalPrizesForChart(officialResults, generatedResults);
  List<String> datesForChart = getDatesForChart(officialResults, generatedResults);

  print('Total Prizes for Chart:');
  print(totalPrizesForChart);

  print('Dates for Chart:');
  print(datesForChart);

  print('\n\n\n\n\n\n\n\n');
}
