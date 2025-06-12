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

        //✅ POST al backend
        $resp = Http::post(
            url("/api/conversations/{$this->activeConversation}/messages"),
            ['content' => $content, 'sender' => 'user']
        );

        if ($resp->successful() && $payload = $resp->json()) {
            // ✅ deduplica: non aggiungere se l’id è già presente
            $already = collect($this->messages)->contains(fn ($m) => $m['id'] === $payload['id']);

            if (! $already) {
                $this->messages[] = $payload;   // un solo record: quello dell’utente
            }

            $this->newMessage = '';             // svuota l’input
        }

        $this->isSending = false;               // sblocca l’invio successivo
        /* Nessun refresh immediato.
        Il wire:poll (o l’SSE) mostrerà la risposta al giro successivo */
        $this->refreshMessages();   
    }

    public function render() { return view('livewire.chat-assistant'); }
}
