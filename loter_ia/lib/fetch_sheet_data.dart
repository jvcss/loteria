import 'package:http/http.dart' as http;
import 'package:csv/csv.dart';

// Função para buscar dados do Google Sheets
Future<List<Map<String, dynamic>>> fetchSheetData(String sheetUrl) async {
  try {
    // Faz o request para a URL pública do CSV
    final response = await http.get(Uri.parse(sheetUrl));

    if (response.statusCode == 200) {
      // Converte o conteúdo CSV em uma lista de mapas
      final csvData = const CsvToListConverter(
        shouldParseNumbers: false, // Permite processar os números manualmente
        fieldDelimiter: ',',
        eol: '\n',
      ).convert(response.body);

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

// Função para processar os dados e garantir o formato correto
Future<List<Map<String, dynamic>>> resultadosOficiais() async {
  // Substitua com o link da sua planilha pública em formato CSV
  const String sheetUrl =
      'https://docs.google.com/spreadsheets/d/17lBepq9eX-O0nrFmNQ14gCKhBUHSsTLCUgDyqJIWOBw/export?format=csv';


  try {
    // Busca e processa os dados
    List<Map<String, dynamic>> sheetData = await fetchSheetData(sheetUrl);

    // Converte os dados para o formato necessário, tratando erros de tipo
    return sheetData.map((row) {
      //print('ROW   - $row'); 
      return {
        'Date': row['Date']?.toString() ?? '11/03/1996',
        'Bola1': int.tryParse(row['Bola1'] ?? '0') ?? 0,
        'Bola2': int.tryParse(row['Bola2'] ?? '0') ?? 0,
        'Bola3': int.tryParse(row['Bola3'] ?? '0') ?? 0,
        'Bola4': int.tryParse(row['Bola4'] ?? '0') ?? 0,
        'Bola5': int.tryParse(row['Bola5'] ?? '0') ?? 0,
        'Bola6': int.tryParse(row['Bola6'] ?? '0') ?? 0,
      };
    }).toList();
  } catch (e) {
    throw Exception('Erro ao processar resultados oficiais: $e');
  }
}
