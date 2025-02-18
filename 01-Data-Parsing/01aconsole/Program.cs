using System;
using System.Collections.Generic;
using System.IO;
using System.Xml.Linq;
using System.Text.Json;
using YamlDotNet.Serialization;
using CsvHelper;
using System.Globalization;

class Program01a
{
    static void Main()
    {
        string basePath = @"C:\Users\eqwoa\Desktop\System-Integration-Mandatory-Assignments\01-Data-Parsing";  // basepath fordi at filerne ikke ligger i samme folder som projektet


        //simpel da ingen serialization nødvendig
        Console.WriteLine("Text File:");
        Console.WriteLine(string.Join("\n", ParseText(Path.Combine(basePath, "about-me.txt"))));

        //massere af serializations, kommentar på hver metoder der forklarer hvad de gør, hover over metode hvis der ikke skal scrolles ned
        Console.WriteLine("\nJSON File:");
        Console.WriteLine(JsonSerializer.Serialize(ParseJson(Path.Combine(basePath, "about-me.json")), new JsonSerializerOptions { WriteIndented = true }));

        Console.WriteLine("\nYAML File:");
        Console.WriteLine(JsonSerializer.Serialize(ParseYaml(Path.Combine(basePath, "about-me.yaml")), new JsonSerializerOptions { WriteIndented = true }));

        Console.WriteLine("\nCSV File:");
        Console.WriteLine(JsonSerializer.Serialize(ParseCsv(Path.Combine(basePath, "about-me.csv")), new JsonSerializerOptions { WriteIndented = true }));

        Console.WriteLine("\nXML File:");
        Console.WriteLine(JsonSerializer.Serialize(ParseXml(Path.Combine(basePath, "about-me.xml")), new JsonSerializerOptions { WriteIndented = true }));
    }

    //parser text og læser alle linjerne før den smider det ind i en liste af strings
    static List<string> ParseText(string filePath) => new List<string>(File.ReadAllLines(filePath));

    //smider det ind i en dictionary i stedet da det gør søgning bedre i et større json objekt, ikke nødvendigt for den nuværende data i json
    static Dictionary<string, object> ParseJson(string filePath) => JsonSerializer.Deserialize<Dictionary<string, object>>(File.ReadAllText(filePath));

    //yaml kræver spøjst nok en nuget package (yamldotnet) da det ikke er en indbygget funktion i dotnet
    static object ParseYaml(string filePath)
    {
        var deserializer = new DeserializerBuilder().Build();
        return deserializer.Deserialize<object>(File.ReadAllText(filePath));
    }


    /* 
    csv er bøvlet, trimmer header i tilfælde af spacing som i mit eget eksempel, ikke nødvendigt hvis god csv korrektur, kræver yderliger en nuget package (csvhelper)
    */
    static List<Person> ParseCsv(string filePath)
    {
        using var reader = new StreamReader(filePath);
        var csvConfig = new CsvHelper.Configuration.CsvConfiguration(CultureInfo.InvariantCulture)
        {
            HeaderValidated = null, // Ignore header validation
            MissingFieldFound = null // Ignore missing field validation
        };

        using var csv = new CsvReader(reader, csvConfig);

        csv.Read();
        csv.ReadHeader();
        var headers = csv.HeaderRecord;
        for (int i = 0; i < headers.Length; i++)
        {
            headers[i] = headers[i].Trim();  // Trimmer headers i tilfælde af spacing issues (ikke optimalt)
        }

        return new List<Person>(csv.GetRecords<Person>());
    }

    /*
    tager filepath og bruger .load til at hente indholdet
    indlæser dataen ind i en dictionary format da det er bedre end lists i det her tilfælde til lookups
    kører gennem foreach loop hvor resultetet er values fundet inde i root
    returnerer result til sidst hvilket er dataen fra vores xml
    */
    static Dictionary<string, string> ParseXml(string filePath)
    {
        var doc = XDocument.Load(filePath);
        var root = doc.Root;
        var result = new Dictionary<string, string>();
        foreach (var element in root.Elements())
        {
            result[element.Name.LocalName] = element.Value;
        }
        return result;
    }
}

public class Person
{
    public string? Name { get; set; }  // Nullable property
    public string? Text { get; set; }  // Nullable property
}
