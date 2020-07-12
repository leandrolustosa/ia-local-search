using System.Collections.Generic;
using VisualizadorDinamicoGraficos.Models.Dtos;

namespace VisualizadorDinamicoGraficos.Models
{
    public class LocalSearchModel
    {
        public string Problema { get; set; }
        public string Algoritmo { get; set; }
        public string Versao { get; set; }
        public string Velocidade { get; set; }

        public NodeModel Estado { get; set; }
        public double Valor { get; set; }

        public double ValorInicial { get; set; }
        public double ValorFinal { get; set; }        

        public List<NodeModel> PopulacaoInicial { get; set; }
        public List<NodeModel> Coordenadas { get; set; }

        public List<ExecucaoModel> Execucoes { get; set; }
        public int NumeroTotalExecucoes { get; set; }
    }
}
