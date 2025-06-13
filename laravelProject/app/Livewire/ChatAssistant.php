<?php

namespace App\Livewire;

use Livewire\Component;
use Illuminate\Support\Facades\Http;
use App\Services\ConversationApi; // Assicurati di avere questo servizio

class ChatAssistant extends Component
{
    /* ---------- Stato ---------- */
    public array  $conversations      = [];
    public ?int   $activeConversation = null;
    public array  $messages           = [];
    public string $newMessage         = '';
    public bool   $isSending          = false;

    /* ---------- MODALE ---------- */
    public ?int   $newConversationActive = null;
    public bool   $showModal          = false;
    public string $newConversationTitle = '';

    /* ---------- Metodi per il modal ---------- */
    public function openModal(): void   { $this->showModal = true;  }
    public function closeModal(): void  { $this->showModal = false; }

    public function createConversation(): void
    {   
        $conversationApi = app(ConversationApi::class);
        // valida, salva, ecc. – esempio minimale:
        $response = $conversationApi->create($this->newConversationTitle);

        if ($response->successful()) {
            $this->conversations[]      = $response->json();
            $this->newConversationTitle = '';
            $this->showModal            = false;
        }
    }

    /* ---------- Mount ---------- */
    public function mount(): void
    {
        $r = Http::get(url('/api/conversations'));
        if ($r->successful()) {
            $this->conversations      = $r->json();
            $this->activeConversation = $this->conversations[0]['id'] ?? null;
            $this->refreshMessages();
        }
    }

    /* ---------- Selezione chat ---------- */
    public function selectConversation(int $id): void
    {
        $this->activeConversation = $id;
        $this->refreshMessages();
    }

    /* ---------- Ricarica ---------- */
    public function refreshMessages(): void
    {
        if (!$this->activeConversation) return;

        $r = Http::get(url("/api/conversations/{$this->activeConversation}/messages"));
        if ($r->successful()) $this->messages = $r->json();
    }

    /* ---------- Invio ---------- */
    public function sendMessage(): void
    {   
        $conversationApi = app(ConversationApi::class);

        // ⛔ evita invii multipli finché la richiesta precedente non è finita
        if ($this->isSending) {
            return;
        }
        $this->isSending = true;

        // ⛔ messaggio vuoto o conversazione non selezionata
        $content = trim($this->newMessage);
        if ($content === '' || ! $this->activeConversation) {
            $this->isSending = false;
            return;
        }

        // ← MODIFICA: push immediato del messaggio dell’utente
        $this->messages[] = [
            'id'      => uniqid('tmp_user_', true),
            'content' => $content,
            'sender'  => 'user',
        ];

        // ← MODIFICA: push del placeholder “Sto pensando…”
        $this->messages[] = [
            'id'      => uniqid('tmp_thinking_', true),
            'content' => 'Sto pensando...',
            'sender'  => 'assistant',
        ];

        // svuoto subito l’input
        $this->newMessage = '';

        
        $conversationApi->sendChat($this->activeConversation, $content, 'user');

        $this->isSending = false; // sblocca l’invio successivo

        // ← RIMOSSA: tolta la chiamata a refreshMessages() qui, 
        // perché ora il wire:poll gestisce il fetch periodico
    }



    public function render() { return view('livewire.chat-assistant'); }
}
