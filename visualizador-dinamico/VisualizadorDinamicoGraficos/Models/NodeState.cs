using System.Text.Json.Serialization;

namespace VisualizadorDinamicoGraficos.Models
{
    public class NodeState
    {
        [JsonPropertyName("py/state")]
        public NodeRoot Root { get; set; }
    }
}
