import { Controller } from "@hotwired/stimulus"

export default class extends Controller {
  static targets = [
    "input", 
    "response", 
    "status", 
    "statusDot", 
    "statusText",
    "advancedFilters",
    "advancedToggleText",
    "advancedToggleIcon"
  ]
  static values = {
    ollamaUrl: String,
    ollamaModel: String
  }

  connect() {
    this.checkAIAvailability()
    this.initializeUserContext()
    
    // Auto-show traditional filters if any are already active
    const hasActiveFilters = document.querySelector('[name="functions[]"]:checked, [name="layers[]"]:checked, [name="min_zone"], [name="max_zone"]')
    if (hasActiveFilters) {
      this.toggleAdvancedFilters()
    }
  }

  async checkAIAvailability() {
    try {
      const response = await fetch('/api/v1/gpt/status', {
        headers: {
          'Cache-Control': 'no-cache',
          'Pragma': 'no-cache'
        }
      })
      const data = await response.json()
      
      this.updateAIStatus(data.success && data.data.llm_available, data.data?.model)
    } catch (error) {
      console.error('AI availability check failed:', error)
      this.updateAIStatus(false)
    }
  }

  updateAIStatus(available, model = null) {
    if (available) {
      this.statusTarget.classList.remove('bg-yellow-100', 'text-yellow-800')
      this.statusTarget.classList.add('bg-green-100', 'text-green-800')
      this.statusDotTarget.classList.remove('bg-yellow-500')
      this.statusDotTarget.classList.add('bg-green-500')
      this.statusTextTarget.textContent = `AI Online (${model})`
    } else {
      this.statusTarget.classList.remove('bg-green-100', 'text-green-800')
      this.statusTarget.classList.add('bg-yellow-100', 'text-yellow-800')
      this.statusDotTarget.classList.remove('bg-green-500')
      this.statusDotTarget.classList.add('bg-yellow-500')
      this.statusTextTarget.textContent = 'AI Offline - Using search fallback'
    }
  }

  async performSearch() {
    const query = this.inputTarget.value.trim()
    if (!query) return

    this.showLoadingState()

    try {
      const response = await fetch('/api/v1/permie_gpt/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRF-Token': document.querySelector('meta[name="csrf-token"]').content
        },
        body: JSON.stringify({
          query: query,
          location: this.userContext.location,
          zone: this.userContext.zone,
          soil: this.userContext.soil,
          experience_level: this.userContext.experience,
          goals: this.userContext.goals
        })
      })

      const data = await response.json()
      
      if (data.success) {
        this.showResponse(data.data)
      } else {
        this.showError('Sorry, I encountered an error while searching. Let me try a traditional search instead.')
      }
    } catch (error) {
      console.error('AI search error:', error)
      this.showError('Sorry, there was an error with the AI search. Falling back to traditional search.')
    } finally {
      this.hideLoadingState()
    }
  }

  showLoadingState() {
    this.inputTarget.disabled = true
    this.statusTextTarget.textContent = 'Searching...'
  }

  hideLoadingState() {
    this.inputTarget.disabled = false
    this.checkAIAvailability()
  }

  showResponse(data) {
    this.responseTarget.classList.remove('hidden')
    this.responseTarget.querySelector('#ai-response-text').innerHTML = this.formatResponse(data)
    this.responseTarget.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
  }

  showError(message) {
    this.responseTarget.classList.remove('hidden')
    this.responseTarget.querySelector('#ai-response-text').textContent = message
    this.responseTarget.scrollIntoView({ behavior: 'smooth', block: 'nearest' })
  }

  formatResponse(data) {
    let responseHtml = data.response
    
    if (data.knowledge_gaps && data.knowledge_gaps.length > 0) {
      responseHtml += '\n\n<div class="mt-4 pt-4 border-t border-blue-200">'
      responseHtml += '<h4 class="text-sm font-medium text-blue-900 mb-2">🔍 Knowledge Gaps Identified:</h4>'
      responseHtml += '<ul class="text-sm text-blue-800 space-y-2">'
      data.knowledge_gaps.forEach(gap => {
        responseHtml += `<li>• ${gap.gap} — ${gap.recommendation}</li>`
      })
      responseHtml += '</ul></div>'
    }
    
    return responseHtml
  }

  closeResponse() {
    this.responseTarget.classList.add('hidden')
  }

  setSearchQuery(event) {
    const query = event.currentTarget.dataset.aiSearchQueryParam
    this.inputTarget.value = query
    this.performSearch()
  }

  toggleAdvancedFilters() {
    this.advancedFiltersTarget.classList.toggle('hidden')
    
    if (this.advancedFiltersTarget.classList.contains('hidden')) {
      this.advancedToggleTextTarget.textContent = 'Show Traditional Filters'
      this.advancedToggleIconTarget.style.transform = 'rotate(0deg)'
    } else {
      this.advancedToggleTextTarget.textContent = 'Hide Traditional Filters'
      this.advancedToggleIconTarget.style.transform = 'rotate(180deg)'
    }
  }

  openAIChat() {
    window.open('/plants/gpt_chat', '_blank')
  }

  async initializeUserContext() {
    try {
      const storedContext = localStorage.getItem('userContext')
      if (storedContext) {
        const parsed = JSON.parse(storedContext)
        if (parsed.lastUpdated && (Date.now() - parsed.lastUpdated < 24 * 60 * 60 * 1000)) {
          this.userContext = parsed
          return
        }
      }

      const response = await fetch('https://ipapi.co/json/')
      const data = await response.json()
      
      this.userContext = {
        location: data.city,
        zone: this.detectZone(data.latitude, data.longitude),
        soil: null,
        experience: 'Beginner',
        goals: ['Sustainable garden', 'Biodiversity'],
        lastUpdated: Date.now()
      }

      localStorage.setItem('userContext', JSON.stringify(this.userContext))
    } catch (error) {
      console.error('Failed to initialize user context:', error)
      this.userContext = {
        location: null,
        zone: null,
        soil: null,
        experience: 'Beginner',
        goals: ['Sustainable garden', 'Biodiversity'],
        lastUpdated: Date.now()
      }
    }
  }

  detectZone(lat, lon) {
    const zone = Math.floor((lat + 90) / 10)
    return `${zone}a`
  }
} 