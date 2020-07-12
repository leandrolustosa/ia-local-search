using System.Text.Json.Serialization;

namespace VisualizadorDinamicoGraficos.Models
{
    public class Configuracao
    {
        [JsonIgnore]
        [JsonPropertyName("py/object")]
        public string Tipo { get; set; }
        public string ArquivoCidades { get; set; }

    }
}
