using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace VisualizadorDinamicoGraficos.Models
{
    public class NodeRoot
    {
        [JsonIgnore]
        [JsonPropertyName("py/object")]
        public string Tipo { get; set; }
        public List<Node> Populacao { get; set; }
        public Node State { get; set; }
        public double Best { get; set; }
        public double Value { get; set; }
    }
}
