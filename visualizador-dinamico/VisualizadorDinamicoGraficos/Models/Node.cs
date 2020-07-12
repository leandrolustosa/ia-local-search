using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace VisualizadorDinamicoGraficos.Models
{
    public class Node
    {
        [JsonIgnore]
        [JsonPropertyName("py/object")]
        public string Tipo { get; set; }        
        public double? X { get; set; }
        public double? Y { get; set; }
        [JsonIgnore]
        public List<Node> Coordenadas { get; set; }
        public List<int> OrdemVisitacao { get; set; }
    }
}
