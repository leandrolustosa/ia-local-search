using System.Text.Json.Serialization;

namespace VisualizadorDinamicoGraficos.Models
{
    public class Execucao
    {
        [JsonIgnore]
        [JsonPropertyName("py/object")]
        public string Tipo { get; set; }
        public int Iteracao { get; set; }
        public NodeState Atual { get; set; }
    }
}
