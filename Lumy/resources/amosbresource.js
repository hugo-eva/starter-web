/**
 * Amos Resource Management System
 * Gerencia recursos e funcionalidades do sistema Lumy TV
 */

class AmosResource {
    constructor() {
        this.resources = new Map();
        this.initialized = false;
    }

    /**
     * Inicializa o sistema de recursos
     */
    init() {
        if (this.initialized) return;
        
        console.log('Amos Resource System initialized');
        this.initialized = true;
        
        // Carrega recursos padrão
        this.loadDefaultResources();
    }

    /**
     * Carrega recursos padrão do sistema
     */
    loadDefaultResources() {
        this.addResource('theme', {
            current: 'light',
            available: ['light', 'dark', 'auto']
        });
        
        this.addResource('language', {
            current: 'en',
            available: ['en', 'pt']
        });
        
        this.addResource('features', {
            digitalSignage: true,
            realTimeUpdates: true,
            automation: true,
            analytics: true
        });
    }

    /**
     * Adiciona um recurso ao sistema
     */
    addResource(name, data) {
        this.resources.set(name, data);
        console.log(`Resource '${name}' added:`, data);
    }

    /**
     * Obtém um recurso do sistema
     */
    getResource(name) {
        return this.resources.get(name);
    }

    /**
     * Atualiza um recurso existente
     */
    updateResource(name, data) {
        if (this.resources.has(name)) {
            const current = this.resources.get(name);
            const updated = { ...current, ...data };
            this.resources.set(name, updated);
            console.log(`Resource '${name}' updated:`, updated);
            return true;
        }
        return false;
    }

    /**
     * Remove um recurso do sistema
     */
    removeResource(name) {
        if (this.resources.has(name)) {
            this.resources.delete(name);
            console.log(`Resource '${name}' removed`);
            return true;
        }
        return false;
    }

    /**
     * Lista todos os recursos disponíveis
     */
    listResources() {
        return Array.from(this.resources.keys());
    }

    /**
     * Verifica se um recurso existe
     */
    hasResource(name) {
        return this.resources.has(name);
    }

    /**
     * Obtém estatísticas do sistema
     */
    getStats() {
        return {
            totalResources: this.resources.size,
            initialized: this.initialized,
            resourceNames: this.listResources()
        };
    }
}

// Cria instância global
window.amosResource = new AmosResource();

// Auto-inicializa quando o DOM estiver pronto
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.amosResource.init();
    });
} else {
    window.amosResource.init();
}

// Exporta para uso em módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AmosResource;
}