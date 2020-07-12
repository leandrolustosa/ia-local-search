chartCreated = false;
interval = null;
indexAnterior = null;
populacaoTSP = null;
stateTSP = null;

function funcaoObjetivo1(x) {
    return Math.pow(x, 2) / 100 + 10 * Math.sin(x - Math.PI / 2);
}

function funcaoObjetivo2(x, y) {
    return 20 + (Math.pow(x, 2) - 10 * Math.cos(2 * Math.PI * x)) + (Math.pow(y, 2) - 10 * Math.cos(2 * Math.PI * y));
}

function criarGrafico1(data) {

    var trace1 = {
        x: data.x,
        y: data.y,
        mode: 'lines',
        type: 'scatter',
        name: 'função objetivo'
    };

    var trace2 = {
        x: [data.xAtual],
        y: [data.yAtual],
        mode: 'markers',
        type: 'scatter',
        name: (data.xp && data.yp) ? 'melhor indivíduo' : 'melhor valor',
        marker: {
            size: 15
        }
    }

    var dados = [trace1, trace2];

    if (data.xp && data.yp) {
        var trace3 = {
            x: data.xp,
            y: data.yp,
            mode: 'markers',
            type: 'scatter',
            name: 'população',
            marker: {
                size: 10
            }
        };

        dados.push(trace3);
    }

    var layout = {
        xaxis: {
            type: 'number',
            title: 'Intervao'
        },
        yaxis: {
            title: 'Função Objetivo'
        },
        title: 'Visualização dos pontos dinamicamente',
        width: 1000,
        height: 800,
    };

    Plotly.newPlot('local-search-chart', dados, layout);

    chartCreated = true;
}

function criarGrafico2(data) {

    var trace1 = {
        opacity: 0.15,
        x: data.x,
        y: data.y,
        z: data.z,
        type: 'mesh3d',
        intensity: data.z,
        colorscale: [
            [0, 'rgb(0, 0, 127)'],
            [0.16, 'rgb(0, 0, 255)'],
            [0.33, 'rgb(0, 255, 255)'],
            [0.50, 'rgb(127, 255, 127)'],
            [0.66, 'rgb(255, 255, 0)'],            
            [0.84, 'rgb(255, 0, 0)'],            
            [1, 'rgb(127, 0, 0)']
        ],
        name: 'função objetivo'
    };

    var trace2 = {
        x: [data.xAtual],
        y: [data.yAtual],
        z: [data.zAtual],        
        mode: 'markers',
        type: 'scatter3d',
        name: (data.xp && data.yp && data.zp) ? 'melhor indivíduo' : 'melhor valor',
        marker: {
            color: 'rgb(0, 0, 0)',
            size: 15
        }
    }

    var dados = [trace1, trace2];

    if (data.xp && data.yp && data.zp) {
        var trace3 = {
            x: data.xp,
            y: data.yp,
            z: data.zp,
            mode: 'markers',
            type: 'scatter3d',            
            name: 'população',
            marker: {
                color: 'rgb(255, 0, 0)',
                size: 10
            }
        };

        dados.push(trace3);
    }

    var layout = {
        xaxis: {
            type: 'number',
            title: 'Intervao',
            range: [-5.12, 5.12]
        },
        yaxis: {
            type: 'number',
            title: 'Função objetivo',
            range: [-5.12, 5.12]
        },
        scene: {
            camera: {
                eye: { x: 1, y: 1.1, z: 0.55 }
            }
        },
        width: 1000,
        height: 800,
        title: 'Visualização dos pontos dinamicamente'
    };

    Plotly.newPlot('local-search-chart', dados, layout);

    chartCreated = true;
}

function criarGrafico3(data) {
    
    var trace1 = {
        x: data.x,
        y: data.y,
        mode: 'markers',
        type: 'scatter',
        marker: {
            size: 12
        }
    };

    var path = d3.path();
    for (i = 0; i < data.x.length; i++) {
        if (i == 0) {
            path.moveTo(data.x[i], data.y[i]);
        }
        else {
            path.lineTo(data.x[i], data.y[i]);
        }
    }
    path.closePath();

    var layout = {
        title: 'Visualização dos pontos dinamicamente',
        width: 1000,
        height: 800,
        shapes: [
            {
                type: 'path',
                path: path.toString()
            }
        ]
    };

    var data = [trace1];

    Plotly.newPlot('local-search-chart', data, layout);
}

function addData(x, y, xp, yp) {
    $("#lblValorInicial").val(y);
    Plotly.animate('local-search-chart', {
        data: [{ x: [x], y: [y] }],
        traces: [1],
        layout: {}
    }, {
        transition: {
            duration: 0,
            easing: 'cubic-in-out'
        },
        frame: {
            duration: 0
        }
    });
    if (xp && yp) {
        Plotly.animate('local-search-chart', {
            data: [{ x: xp, y: yp }],
            traces: [2],
            layout: {}
        }, {
            transition: {
                duration: 0,
                easing: 'cubic-in-out'
            },
            frame: {
                duration: 0
            }
        });
    }
}

function addData3D(x, y, z, xp, yp, zp) {
    $("#lblValorInicial").val(z);
    Plotly.animate('local-search-chart', {
        data: [{ x: [x], y: [y], z: [z] }],
        traces: [1],
        layout: {
            xaxis2: { overlaying: true },
            yaxis2: { overlaying: true },
            zaxis2: { overlaying: true }
        }
    }, {
        transition: {
            duration: 0,
            easing: 'cubic-in-out'
        },
        frame: {
            duration: 0
        }
    });

    if (xp && yp && zp) {
        Plotly.animate('local-search-chart', {
            data: [{ x: xp, y: yp, z: zp }],
            traces: [2],
            layout: {}
        }, {
            transition: {
                duration: 0,
                easing: 'cubic-in-out'
            },
            frame: {
                duration: 0
            }
        });
    }
}

function addPath(data) {
    $("#lblValorInicial").val(data.distancia);
    var path = d3.path();
    for (i = 0; i < data.x.length; i++) {
        if (i == 0) {
            path.moveTo(data.x[i], data.y[i]);
        }
        else {
            path.lineTo(data.x[i], data.y[i]);
        }
    }
    path.closePath();

    var layout = {
        title: 'Visualização dos pontos dinamicamente',
        width: 1000,
        height: 800,
        shapes: [

            //Filled Polygon

            {
                type: 'path',
                path: path.toString()
            }
        ]
    };

    Plotly.animate('local-search-chart', {
        data: [{ x: data.x, y: data.y }],
        traces: [0],
        layout: layout
    }, {
        transition: {
            duration: 0,
            easing: 'cubic-in-out'
        },
        frame: {
            duration: 0
        }
    })
}

async function setIntervalGraficoTSP(data, dadosExecucao, contador, velocidade) {
    var execucao = 0;
    var dadosExecucao = dadosExecucao;
    return setInterval(async function () {
        var atual = null;
        try {
            atual = dadosExecucao[execucao].atual;
        }
        catch (e) {
            if (execucao == 1000) {
                execucao = 998;
            }
            else {
                clearInterval(interval);
            }
        }

        execucao++;

        if ((contador * execucao + execucao) === data.numeroTotalExecucoes) {
            clearInterval(interval);
        }

        if ((contador * execucao + execucao + 1) % 1000 === 0) {
            clearInterval(interval);

            execucao = 0;
            contador++;

            const result = await $.ajax("dados/getdadospaginado/?pagina=" + contador.toString(), {
                contentType: "application/json",
                type: "get",
                dataType: "json"
            });

            dadosExecucao = result;

            interval = setIntervalGraficoTSP(data, dadosExecucao, contador, velocidade);

            return;
        }

        if (atual.populacao != null && atual.populacao.length != 0) {
            populacaoTSP = atual.populacao;
            for (var p = 0; p < atual.populacao.length; p++) {
                dadosExecucao[execucao].atual.state = atual.populacao[p];
            }
        }

        if (populacaoTSP == null && !atual.state) {
            return;
        }

        if (populacaoTSP != null && populacaoTSP.length != 0) {
            nodes = dadosExecucao.filter(x => x.atual.value === atual.best);
            if (nodes[0] && nodes[0].atual.state) {
                stateTSP = nodes[0].atual.state;
            }
        }
        else {
            stateTSP = atual.state;
        }

        var dados = {
            x: stateTSP.ordemVisitacao.map(indice => data.coordenadas[indice].x),
            y: stateTSP.ordemVisitacao.map(indice => data.coordenadas[indice].y),
            distancia: atual.best
        };
        dados.x.splice(0, 0, data.coordenadas[0].x);
        dados.y.splice(0, 0, data.coordenadas[0].y);

        addPath(dados);

    }, velocidade);
}

function arraysEqual(a1, a2) {    
    return JSON.stringify(a1) == JSON.stringify(a2);
}

$(document).ready(function () {
    $(".btn-atualizar").click(async function () {
        var selProblema = $("#selProblema");
        var selAlgoritmo = $("#selAlgoritmo");
        var selVersao = $("#selVersoes");
        var selVelocidades = $("#selVelocidades");
        var rdoIteracao = $("input[name=iteracaoRadios]:checked");

        if (!selProblema.val() || !selAlgoritmo.val()) {
            alert("Informa o problema e o algoritmo");
        }

        $.ajax("dados/?problema=" + selProblema.val() + "&algoritmo=" + selAlgoritmo.val() + "&versao=" + selVersao.val() + "&iteracao=" + rdoIteracao.val(), {
            contentType: "application/json",
            type: "get",
            dataType: "json",            
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                alert("erro");
            },
            success: async function (data, textStatus, XMLHttpRequest) {
                $("#lblValorInicial").val(data.valorInicial);
                $("#lblValorFinal").val(data.valorFinal);

                if (chartCreated) {
                    clearInterval(interval);
                    Plotly.purge("local-search-chart");
                }

                if (selProblema.val() === "problema-1") {
                    var populacaoInicial = null, estadoInicial = null;
                    if (data.populacaoInicial !== null && data.populacaoInicial.length != 0) {
                        for (var p = 0; p < data.populacaoInicial.length; p++) {
                            data.execucoes[p].atual.estado = data.populacaoInicial[p];
                        }
                        var nodesInicial = data.execucoes.filter(x => x.atual.value === data.valor);
                        estadoInicial = nodesInicial[0].atual.estado;
                        populacaoInicial = data.populacaoInicial.filter(obj => obj.x !== estadoInicial.x);
                    }
                    var dados = {
                        x: [],
                        y: [],
                        xAtual: populacaoInicial !== null ? estadoInicial.x : data.estado.x,
                        yAtual: data.valor,
                        xp: populacaoInicial !== null ? populacaoInicial.map(obj => obj.x) : null,
                        yp: populacaoInicial !== null ? populacaoInicial.map(obj => funcaoObjetivo1(obj.x)) : null
                    };

                    for (var i = 0; i < 202; i++) {
                        dados.x.push(i - 100);
                        dados.y.push(funcaoObjetivo1(i - 100));
                    }
                    criarGrafico1(dados);

                    var velocidade = parseInt(selVelocidades.val());

                    var execucao = 0;
                    var populacao = null;
                    var state = null;
                    interval = setInterval(function () {
                        var atual = data.execucoes[execucao].atual;
                        execucao++;
                        if (execucao === data.execucoes.length) {
                            clearInterval(interval);
                        }
                        
                        var xp, yp = null;

                        if (atual.populacao != null && atual.populacao.length != 0) {
                            populacao = atual.populacao;
                            for (var p = 0; p < atual.populacao.length; p++) {
                                data.execucoes[execucao].atual.state = atual.populacao[p];
                            }
                        }

                        if (populacao == null && !atual.state) {
                            return;
                        }

                        if (populacao != null && populacao.length != 0) {                            
                            xp = populacao.map(obj => obj.x);
                            yp = populacao.map(obj => funcaoObjetivo1(obj.x));

                            nodes = data.execucoes.filter(x => x.atual.value === atual.best);
                            if (nodes[0]) {
                                state = nodes[0].atual.state;
                            }
                        }

                        if (state || atual.state) {
                            addData(xp != null ? state.x : atual.state.x, atual.best, xp, yp);
                        }
                    }, velocidade);
                }
                else if (selProblema.val() === "problema-2") {
                    var populacaoInicial = null, estadoInicial = null;
                    if (data.populacaoInicial !== null && data.populacaoInicial.length != 0) {
                        for (var p = 0; p < data.populacaoInicial.length; p++) {
                            data.execucoes[p].atual.estado = data.populacaoInicial[p];
                        }
                        var nodesInicial = data.execucoes.filter(x => x.atual.value === data.valor);
                        estadoInicial = nodesInicial[0].atual.estado;
                        populacaoInicial = data.populacaoInicial.filter(obj => obj.x !== estadoInicial.x && obj.y !== estadoInicial.y);
                    }
                    var dados = {
                        x: [],
                        y: [],
                        z: [],
                        xAtual: populacaoInicial !== null ? estadoInicial.x : data.estado.x,
                        yAtual: populacaoInicial !== null ? estadoInicial.y : data.estado.y,
                        zAtual: data.valor,
                        xp: populacaoInicial !== null ? populacaoInicial.map(obj => obj.x) : null,
                        yp: populacaoInicial !== null ? populacaoInicial.map(obj => obj.y) : null,
                        zp: populacaoInicial !== null ? populacaoInicial.map(obj => funcaoObjetivo2(obj.x, obj.y)) : null
                    };

                    for (i = 0; i < 65; i++) {
                        var aValor = -5.12 + (0.16 * i);
                        for (j = 0; j < 65; j++) {
                            var bValor = -5.12 + (0.16 * j);
                            dados.x.push(aValor);
                            dados.y.push(bValor);
                            dados.z.push(funcaoObjetivo2(aValor, bValor));
                        }
                    }

                    criarGrafico2(dados);

                    var velocidade = parseInt(selVelocidades.val());

                    var execucao = 0;
                    var populacao = null;
                    var state = null;
                    interval = setInterval(function () {
                        var atual = data.execucoes[execucao].atual;
                        execucao++;
                        if (execucao === data.execucoes.length) {
                            clearInterval(interval);
                        }
                        
                        var xp, yp, zp = null;

                        if (atual.populacao != null && atual.populacao.length != 0) {
                            populacao = atual.populacao;
                            for (var p = 0; p < atual.populacao.length; p++) {
                                data.execucoes[execucao].atual.state = atual.populacao[p];
                            }
                        }

                        if (populacao == null && !atual.state) {
                            return;
                        }

                        if (populacao != null && populacao.length != 0) {                            
                            xp = populacao.map(obj => obj.x);
                            yp = populacao.map(obj => obj.y);
                            zp = populacao.map(obj => funcaoObjetivo2(obj.x, obj.y));

                            nodes = data.execucoes.filter(x => x.atual.value === atual.best);
                            if (nodes[0] && nodes[0].atual.state) {
                                state = nodes[0].atual.state;
                            }
                        }
                        addData3D(xp != null ? state.x : atual.state.x, yp != null ? state.y : atual.state.y, atual.best, xp, yp, zp);
                    }, velocidade);
                }
                else if (selProblema.val() === "problema-3") {
                    var populacaoInicial = null, estadoInicial = null;
                    if (data.populacaoInicial !== null && data.populacaoInicial.length != 0) {
                        for (var p = 0; p < data.populacaoInicial.length; p++) {
                            data.execucoes[p].atual.estado = data.populacaoInicial[p];
                        }
                        var nodesInicial = data.execucoes.filter(x => x.atual.value === data.valor);
                        estadoInicial = nodesInicial[0].atual.estado;
                        populacaoInicial = data.populacaoInicial.filter(obj => !arraysEqual(obj.ordemVisitacao, estadoInicial.ordemVisitacao));
                    }
                    else {
                        estadoInicial = data.estado;
                    }

                    var dados = {
                        x: estadoInicial.ordemVisitacao.map(indice => data.coordenadas[indice].x),
                        y: estadoInicial.ordemVisitacao.map(indice => data.coordenadas[indice].y),
                        distancia: data.valor
                    };
                    dados.x.splice(0, 0, data.coordenadas[0].x);
                    dados.y.splice(0, 0, data.coordenadas[0].y);
                    
                    criarGrafico3(dados);

                    var velocidade = parseInt(selVelocidades.val());

                    var execucao = 0;
                    var contador = 0;
                    var dadosExecucao = data.execucoes;                    
                    interval = await setIntervalGraficoTSP(data, dadosExecucao, contador, velocidade);
                }
            }
        });
    });

    $(".btn-atualizar").click();    
});