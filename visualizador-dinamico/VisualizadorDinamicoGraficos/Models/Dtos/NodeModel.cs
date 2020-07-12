using System.Collections.Generic;

namespace VisualizadorDinamicoGraficos.Models.Dtos
{
    public class NodeModel
    {    
        public double? X { get; set; }
        public double? Y { get; set; }
        public List<NodeModel> Coordenadas { get; set; }
        public List<int> OrdemVisitacao { get; set; }

    }
}
