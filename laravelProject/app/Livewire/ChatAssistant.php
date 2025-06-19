<?php

namespace App\Livewire;

use Livewire\Component;
use Illuminate\Support\Facades\Http;
use App\Services\ConversationApi;
use App\Models\Message;
use Livewire\WithPagination;

class ChatAssistant extends Component
{
    use WithPagination;
    
    public int $perPage = 20;

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

    // il service può restituire o un Response o direttamente l’array
    $raw = $conversationApi->create(trim($this->newConversationTitle) ?: null);

    // --- normalizziamo ---
    if ($raw instanceof \Illuminate\Http\Client\Response) {
        if (! $raw->successful()) {
            session()->flash('error', 'Errore nel salvataggio');
            return;
        }
        $conv = $raw->json();              // array normalizzato
    } else {
        // qui se $raw **è già** l’array
        $conv = $raw;
    }

    /* --------  aggiornamento stato UI -------- */
    $this->conversations[]   = $conv;
    $this->activeConversation = $conv['id'];
    $this->messages           = [];
    $this->newConversationTitle = '';
    $this->showModal            = false;
    $this->perPage              = 20;
    $this->resetPage();

    // se vuoi subito i (pochi) messaggi presenti:
    // $this->refreshMessages();
}


    /* ---------- Mount ---------- */
    public function mount(): void
    {
        $conversationApi = app(ConversationApi::class);

        $r = $conversationApi->mount();
        if ($r->successful()) {
            $this->conversations = $r->json();

            // indice dell’ultimo elemento, oppure null se l’array è vuoto
            $lastIndex = array_key_last($this->conversations);

            $this->activeConversation = $lastIndex !== null
                ? $this->conversations[$lastIndex]['id']
                : null;

            $this->refreshMessages();
        }
    }

    /* ---------- Selezione chat ---------- */
    public function selectConversation(int $id): void
    {
        $this->activeConversation = $id;
        $this->refreshMessages();
            $this->perPage = 20;     // torna al valore iniziale
        $this->resetPage();
    }

    /* ---------- Ricarica ---------- */
    public function refreshMessages(): void
    {
        $conversationApi = app(ConversationApi::class);

        if (! $this->activeConversation) {
            return;
        }

        $r = $conversationApi->refresh($this->activeConversation);

        if ($r->successful()) {
            $this->messages = $r->json('data') ?? [];
        }
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

    public function getMessagesProperty()
    {
        return Message::where('conversation_id', $this->activeConversation)
                    ->latest()              // messaggi più recenti
                    ->take($this->perPage)  // limite dinamico
                    ->get()
                    ->reverse();            // dal più vecchio al più nuovo
    }

    public function getHasMoreProperty()
    {
        // vero se in DB ci sono ancora messaggi oltre quelli già mostrati
        return Message::where('conversation_id', $this->activeConversation)
                    ->count() > $this->perPage;
    }

    public function render()
    {
        return view('livewire.chat-assistant', [
            'messages' => $this->messages,              // quelli push-ati in tempo reale
            'loaded'   => $this->getMessagesProperty(),
            'hasMore'  => $this->getHasMoreProperty(),             // accessor per il bottone
        ]);
    }

    public function loadMore(): void
    {
        $this->perPage += 20;   // la prossima render mostrerà 20 record in più
    }
}
