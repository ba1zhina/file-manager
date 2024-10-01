using System;
using System.IO;
using System.IO.Compression;
using System.Xml;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

class Program
{
    static void Main()
    {
        Console.WriteLine("1. Информация о логических дисках:");
        foreach (var drive in DriveInfo.GetDrives())
        {
            if (drive.IsReady)
            {
                Console.WriteLine($"Имя устройства: {drive.Name}");
                Console.WriteLine($"Тип файловой системы: {drive.DriveFormat}");
                Console.WriteLine($"Размер диска: {drive.TotalSize / (1024 * 1024 * 1024):F2} GB");
                Console.WriteLine($"Свободное место: {drive.AvailableFreeSpace / (1024 * 1024 * 1024):F2} GB");
                Console.WriteLine($"Метка тома: {drive.VolumeLabel}");
                Console.WriteLine(new string('-', 40));
            }
        }

        Console.WriteLine("2. Работа с файлами.");
        string fileName = "example.txt";
        Console.Write("Введите строку для записи в файл: ");
        string userInput = Console.ReadLine();

        File.WriteAllText(fileName, userInput);
        Console.WriteLine("\nСодержимое файла:");
        Console.WriteLine(File.ReadAllText(fileName));
        File.Delete(fileName);
        Console.WriteLine("Файл успешно удалён.");
        Console.WriteLine(new string('-', 40));

       
        Console.WriteLine("3. Работа с форматом JSON.");
        string jsonFileName = "data.json";

        Console.Write("Введите ваше имя: ");
        string name = Console.ReadLine();
        Console.Write("Введите ваш возраст: ");
        string age = Console.ReadLine();
        Console.Write("Введите ваш город: ");
        string city = Console.ReadLine();

        var jsonData = new JObject
        {
            ["name"] = name,
            ["age"] = age,
            ["city"] = city
        };

        
        string jsonString = JsonConvert.SerializeObject(jsonData, Newtonsoft.Json.Formatting.Indented);
        File.WriteAllText(jsonFileName, jsonString);  


       
        Console.WriteLine("\nСодержимое JSON файла:");
        Console.WriteLine(File.ReadAllText(jsonFileName));

      
        File.Delete(jsonFileName);
        Console.WriteLine("JSON файл успешно удалён.");
        Console.WriteLine(new string('-', 40));

       
        Console.WriteLine("4. Работа с форматом XML.");
        string xmlFileName = "data.xml";
        if (!File.Exists(xmlFileName))
        {
            using (var xmlWriter = XmlWriter.Create(xmlFileName))
            {
                xmlWriter.WriteStartElement("users");
                xmlWriter.WriteEndElement();
            }
        }

        XmlDocument xmlDoc = new XmlDocument();
        xmlDoc.Load(xmlFileName);

        XmlElement newUser = xmlDoc.CreateElement("user");

        XmlElement nameElem = xmlDoc.CreateElement("name");
        nameElem.InnerText = name;
        newUser.AppendChild(nameElem);

        XmlElement ageElem = xmlDoc.CreateElement("age");
        ageElem.InnerText = age;
        newUser.AppendChild(ageElem);

        XmlElement cityElem = xmlDoc.CreateElement("city");
        cityElem.InnerText = city;
        newUser.AppendChild(cityElem);

        xmlDoc.DocumentElement.AppendChild(newUser);
        xmlDoc.Save(xmlFileName);

        Console.WriteLine("\nСодержимое XML файла:");
        xmlDoc.Load(xmlFileName);
        foreach (XmlNode userNode in xmlDoc.DocumentElement.ChildNodes)
        {
            Console.WriteLine($"Имя: {userNode["name"].InnerText}, Возраст: {userNode["age"].InnerText}, Город: {userNode["city"].InnerText}");
        }

        File.Delete(xmlFileName);
        Console.WriteLine("XML файл успешно удалён.");
        Console.WriteLine(new string('-', 40));

        
        Console.WriteLine("5. Работа с zip-архивами.");
        Console.Write("Введите путь к файлу, который нужно добавить в архив: ");
        string userFile = Console.ReadLine();
        string zipFileName = "my_archive.zip";

        using (ZipArchive zip = ZipFile.Open(zipFileName, ZipArchiveMode.Create))
        {
            zip.CreateEntryFromFile(userFile, Path.GetFileName(userFile));
        }

        Console.WriteLine($"Создан архив: {zipFileName}");
        FileInfo zipFileInfo = new FileInfo(zipFileName);
        Console.WriteLine($"Размер архива: {zipFileInfo.Length} байт");

        string extractFolder = "extracted_files";
        Directory.CreateDirectory(extractFolder);
        ZipFile.ExtractToDirectory(zipFileName, extractFolder);
        Console.WriteLine($"Архив {zipFileName} разархивирован в папку {extractFolder}");

        File.Delete(zipFileName);
        Directory.Delete(extractFolder, true);
        Console.WriteLine("Файл и архив успешно удалены.");
    }
}
