import 'package:http/http.dart' as http;
import 'package:csv/csv.dart';

// Função para buscar dados do Google Sheets
Future<List<Map<String, dynamic>>> fetchSheetData(String sheetUrl) async {
  try {
    // Faz o request para a URL pública do CSV
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

void main() async {
  // Substitua com o link da sua planilha pública em formato CSV
  const String sheetUrl =
      'https://docs.google.com/spreadsheets/d/1YW0Va7hO00TVgoE_i9Yqj3N5Ex3kl1ZHeZJB_3Xsmk4/export?format=csv';

  // Busca e processa os dados
  List<Map<String, dynamic>> sheetData = await fetchSheetData(sheetUrl);

  // Exibe os dados no console
  print('Dados do Google Sheets:');
  for (var row in sheetData) {
    print(row);
  }

  // Você pode agora usar `sheetData` como `officialResults`
  // Exemplo de uso com calculateHitsWithPrizes:
  List<Map<String, dynamic>> officialResults = sheetData.map((row) {
    return {
      'Date': row['Date'],
      'Bola1': int.parse(row['Bola1']),
      'Bola2': int.parse(row['Bola2']),
      'Bola3': int.parse(row['Bola3']),
      'Bola4': int.parse(row['Bola4']),
      'Bola5': int.parse(row['Bola5']),
      'Bola6': int.parse(row['Bola6']),
    };
  }).toList();

  print('Resultados Oficiais Formatados:');
  print(officialResults);
  print('\n\n\n\n\n\n\n\n:');
  print('\n\n\n\n\n\n\n\n:');
}
