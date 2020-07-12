using AutoMapper;
using VisualizadorDinamicoGraficos.Models.Dtos;

namespace VisualizadorDinamicoGraficos.Models.AutoMapperConfig
{
    public class AutoMapperGraficosConfigurator : Profile
    {
        public AutoMapperGraficosConfigurator()
        {
            CreateMap<Execucao, ExecucaoModel>()
                .ForMember(p => p.Atual, o => o.MapFrom(t => t.Atual.Root));

            CreateMap<NodeRoot, NodeRootModel>();

            CreateMap<Node, NodeModel>();
        }
    }
}
