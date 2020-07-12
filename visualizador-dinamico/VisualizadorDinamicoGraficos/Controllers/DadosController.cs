using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using AutoMapper;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Caching.Memory;
using Microsoft.Extensions.Logging;
using VisualizadorDinamicoGraficos.Models;
using VisualizadorDinamicoGraficos.Models.Dtos;

namespace VisualizadorDinamicoGraficos.Controllers
{
    [ApiController]
    [Route("[controller]")]
    public class DadosController : ControllerBase
    {
        private const string CACHE_KEY = "execucoes";
        private const int TAMANHO_PAGINA = 1000;

        private readonly IMapper _mapper;
        private readonly ILogger<DadosController> _logger;
        private readonly IWebHostEnvironment _env;
        private readonly IMemoryCache _cache;
        
        public DadosController(IMemoryCache cache, IMapper mapper, ILogger<DadosController> logger, IWebHostEnvironment env)
        {
            _cache = cache;
            _mapper = mapper;
            _logger = logger;
            _env = env;
        }

        [HttpGet]
        public LocalSearchModel Get(string problema, string algoritmo, string versao, string iteracao)
        {
            var pathRoot = _env.ContentRootPath;
            var pathDados = Path.Combine(pathRoot, $"dados\\{problema}\\{versao}");
            var pathArquivoConfiguracoes = Path.Combine(pathRoot, $"dados\\configuracoes\\{problema}-configuracao-{versao}.cfg");

            var textoArquivoConfig = System.IO.File.ReadAllText(Path.Combine(pathRoot, pathArquivoConfiguracoes));
            var configuracao = JsonSerializer.Deserialize<Configuracao>(textoArquivoConfig, new JsonSerializerOptions { PropertyNamingPolicy = JsonNamingPolicy.CamelCase });
            var coordenadas = new List<NodeModel>();
            if (!string.IsNullOrEmpty(configuracao.ArquivoCidades))
            {
                foreach (string linha in System.IO.File.ReadAllLines(Path.Combine(pathRoot, configuracao.ArquivoCidades)))
                {
                    var coords = linha.Split(new[] { " " }, StringSplitOptions.RemoveEmptyEntries);
                    coordenadas.Add(new NodeModel { X = double.Parse(coords[0], System.Globalization.CultureInfo.GetCultureInfo("en-US")), Y = double.Parse(coords[1], System.Globalization.CultureInfo.GetCultureInfo("en-US")) });
                }
            }

            NodeRoot primeiroNode = null;
            NodeRoot bestNode = null;
            NodeRoot ultimoNode = null;
            List<Execucao> execucoes = null;
            if (!string.IsNullOrEmpty(problema) && !string.IsNullOrEmpty(algoritmo) && !string.IsNullOrEmpty(iteracao))
            {
                var pathArquivo = $"{algoritmo}-{iteracao}.dat";
                var textoArquivo = System.IO.File.ReadAllText(Path.Combine(pathDados, pathArquivo));

                execucoes = JsonSerializer.Deserialize<List<Execucao>>(textoArquivo, new JsonSerializerOptions { PropertyNamingPolicy = JsonNamingPolicy.CamelCase });
                primeiroNode = execucoes.First().Atual.Root;
                bestNode = execucoes.First(x => x.Atual.Root.Best == x.Atual.Root.Value).Atual.Root;
                ultimoNode = execucoes.Last().Atual.Root;
            }

            var bestNodeModel = _mapper.Map<NodeRootModel>(bestNode);
            var execucoesModel = _mapper.Map<List<ExecucaoModel>>(execucoes.Select(p => p).ToList());

            _cache.Remove(CACHE_KEY);
            var entry = _cache.Set(CACHE_KEY, execucoesModel);            

            var model = new LocalSearchModel
            {
                Algoritmo = algoritmo,
                Problema = problema,
                Estado = bestNodeModel.State,
                Valor = primeiroNode.Best,
                ValorInicial = primeiroNode.Value,
                ValorFinal = ultimoNode.Best,
                PopulacaoInicial = _mapper.Map<List<NodeModel>>(primeiroNode.Populacao),
                Coordenadas = coordenadas,
                Execucoes = execucoesModel.Skip(0).Take(1000).ToList(),
                NumeroTotalExecucoes = execucoesModel.Count
            };

            return model;
        }

        [HttpGet]
        [Route("[action]")]
        public IEnumerable<ExecucaoModel> GetDadosPaginado(int pagina)
        {
            var execucoes = (List<ExecucaoModel>)_cache.Get(CACHE_KEY);

            return execucoes.Skip(pagina*TAMANHO_PAGINA).Take(TAMANHO_PAGINA).ToList();
        }
    }
}
