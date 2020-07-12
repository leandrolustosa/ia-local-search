using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.Json.Serialization;
using System.Threading.Tasks;

namespace VisualizadorDinamicoGraficos.Models.Dtos
{
    public class NodeStateModel
    {
        [JsonPropertyName("py/state")]
        public Node State { get; set; }
    }
}
