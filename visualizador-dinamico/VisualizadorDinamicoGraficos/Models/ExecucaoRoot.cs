using System.Text.Json.Serialization;

namespace VisualizadorDinamicoGraficos.Models
{
    public class ExecucaoRoot
    {
        [JsonIgnore]
        [JsonPropertyName("py/object")]
        public string Tipo { get; set; }
        [JsonPropertyName("py/state")]
        public Execucao Execucao { get; set; }
    }
}
