<?php

namespace App\Livewire;

use Livewire\Component;
use Illuminate\Support\Collection;
use App\Services\ConversationApi;
use App\Models\Message;

class ChatAssistant extends Component
{
    /* ------- Config ------- */
    public int $chunkSize = 20;   // blocco di messaggi da caricare/aggiungere

    /* ------- Stato ------- */
    public Collection $history;   // messaggi già mostrati (vecchio → nuovo)
    public array      $liveStack   = [];   // placeholder (user / “Sto pensando…”)  
    public array      $conversations = [];
    public ?int       $activeConversation = null;
    public string     $newMessage  = '';
    public bool       $isSending   = false;

    /* ------- Modale ------- */
    public bool   $showModal            = false;
    public string $newConversationTitle = '';

    /* ======================= Ciclo di vita ======================= */
    public function mount(): void
    {
        $this->history = collect(); // inizializza la collection vuota

        $conversationApi = app(ConversationApi::class);
        $r = $conversationApi->mount();
        if ($r->successful()) {
            $this->conversations = $r->json();
            $lastIndex = array_key_last($this->conversations);
            $this->activeConversation = $lastIndex !== null ? $this->conversations[$lastIndex]['id'] : null;
            $this->loadLatest();      // carica i 20 più recenti se c’è una chat attiva
        }
    }

    /* ======================= Modale “Nuova chat” ======================= */
    public function openModal(): void   { $this->showModal = true;  }
    public function closeModal(): void  { $this->showModal = false; }

    public function createConversation(): void
    {
        $conversationApi = app(ConversationApi::class);
        $response = $conversationApi->create($this->newConversationTitle);

        if ($response->successful()) {
            $this->conversations[]      = $response->json();
            $this->newConversationTitle = '';
            $this->showModal            = false;
        }
    }

    /* ======================= Cambio chat ======================= */
    public function selectConversation(int $id): void
    {
        $this->activeConversation = $id;
        $this->history   = collect(); // svuota lo storico mostrato
        $this->liveStack = [];        // svuota i placeholder
        $this->loadLatest();          // ricarica gli ultimi 20
    }

    /* ======================= Caricamento iniziale ======================= */
    private function loadLatest(): void
    {
        if (! $this->activeConversation) return;

        $this->history = Message::where('conversation_id', $this->activeConversation)
                                ->latest()          // più recenti in alto
                                ->take($this->chunkSize)
                                ->get()
                                ->reverse();        // ordina internamente da vecchio a nuovo
    }

    /* ======================= Carica altri (più vecchi) ======================= */
    public function loadMore(): void
    {
        if (! $this->activeConversation) return;

        $already = $this->history->count();

        $older = Message::where('conversation_id', $this->activeConversation)
                        ->latest()
                        ->skip($already)            // salta quelli già visti
                        ->take($this->chunkSize)
                        ->get()
                        ->reverse();

        // prepend: i più vecchi vanno in cima
        $this->history = $older->merge($this->history);
    }

    /* ======================= Poll: nuovi messaggi dal server ======================= */
    public function refreshMessages(): void
    {
        if (! $this->activeConversation || $this->history->isEmpty()) return;

        $lastId = $this->history->last()->id;    // id del messaggio più recente già mostrato

        $newer = Message::where('conversation_id', $this->activeConversation)
                        ->where('id', '>', $lastId)
                        ->orderBy('created_at')  // ordine naturale
                        ->get();

        if ($newer->isNotEmpty()) {
            // append: nuovi in fondo
            $this->history = $this->history->merge($newer);
        }
    }

    /* ======================= Invio messaggio ======================= */
    public function sendMessage(): void
    {
        if ($this->isSending) return;            // blocca doppio invio

        $content = trim($this->newMessage);
        if ($content === '' || ! $this->activeConversation) return;

        $this->isSending = true;

        // 1. Placeholder immediati nell’interfaccia
        $this->liveStack[] = [
            'id'      => uniqid('tmp_user_', true),
            'content' => $content,
            'sender'  => 'user',
        ];
        $this->liveStack[] = [
            'id'      => uniqid('tmp_thinking_', true),
            'content' => 'Sto pensando...',
            'sender'  => 'assistant',
        ];

        // 2. Svuota input
        $this->newMessage = '';

        // 3. Chiamata API
        $conversationApi = app(ConversationApi::class);
        $conversationApi->sendChat($this->activeConversation, $content, 'user');

        $this->isSending = false;
    }

    /* ======================= Utility: ci sono altri vecchi? ======================= */
    private function hasMore(): bool
    {
        if (! $this->activeConversation) return false;

        $total = Message::where('conversation_id', $this->activeConversation)->count();
        return $this->history->count() < $total;
    }

    /* ======================= Render ======================= */
    public function render()
    {
        return view('livewire.chat-assistant', [
            'messages' => $this->history->merge($this->liveStack), // storico + placeholder
            'hasMore'  => $this->hasMore(),
        ]);
    }
}
