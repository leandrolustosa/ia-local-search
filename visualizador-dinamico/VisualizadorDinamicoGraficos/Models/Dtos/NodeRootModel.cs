using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace VisualizadorDinamicoGraficos.Models.Dtos
{
    public class NodeRootModel
    {
        public List<NodeModel> Populacao { get; set; }
        public NodeModel State { get; set; }
        public double Best { get; set; }
        public double Value { get; set; }
    }
}
