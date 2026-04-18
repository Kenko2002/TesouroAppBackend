// frontend/static/frontend/js/tesouro_service.js

class TesouroService {
    constructor() {
        this.apiUrl = '/api/tesouro-series/'; // URL da nova API processada
    }

    async fetchTimeSeriesData() {
        try {
            const response = await fetch(this.apiUrl, {
                credentials: 'same-origin', // Para incluir cookies de sessão
            });
            if (!response.ok) {
                throw new Error('Erro ao buscar dados');
            }
            const data = await response.json();
            return data.series || []; // Retorna as séries processadas
        } catch (error) {
            console.error('Erro ao buscar séries temporais:', error);
            return [];
        }
    }

    processDataForChart(seriesData) {
        // Os dados já estão processados pelo backend
        return seriesData.map(series => ({
            label: series.label,
            data: series.data.map(point => ({
                x: new Date(point.x),
                y: point.y
            })),
            borderColor: this.getRandomColor(),
            fill: false
        }));
    }

    getRandomColor() {
        return '#' + Math.floor(Math.random()*16777215).toString(16);
    }

    async getTimeSeriesData() {
        const seriesData = await this.fetchTimeSeriesData();
        return this.processDataForChart(seriesData);
    }
}

// Exportar para uso global
window.TesouroService = TesouroService;