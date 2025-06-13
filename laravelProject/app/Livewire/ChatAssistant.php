<?php

namespace App\Livewire;

use Livewire\Component;
use Illuminate\Support\Facades\Http;

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
    /** Flag che decide se mostrare il modal */
    public bool   $showModal          = false;
    /** Campo “Titolo” dentro al modal  */
    public string $newConversationTitle = '';

    /* ---------- Metodi per il modal ---------- */
    public function openModal(): void   { $this->showModal = true;  }
    public function closeModal(): void  { $this->showModal = false; }

    public function createConversation(): void
    {
        // valida, salva, ecc. – esempio minimale:
        $r = Http::post(url('/api/conversations'), [
            'title' => $this->newConversationTitle,
        ]);

        if ($r->successful()) {
            // aggiorna la lista (o chiama un refresh generale)
            $this->conversations[] = $r->json();
            // pulizia UI
            $this->newConversationTitle = '';
            $this->showModal = false;
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

        // ✅ POST al backend
        Http::post(
            url("/api/conversations/{$this->activeConversation}/messages"),
            ['content' => $content, 'sender' => 'user']
        );

        $this->isSending = false; // sblocca l’invio successivo

        // ← RIMOSSA: tolta la chiamata a refreshMessages() qui, 
        // perché ora il wire:poll gestisce il fetch periodico
    }



    public function render() { return view('livewire.chat-assistant'); }
}
