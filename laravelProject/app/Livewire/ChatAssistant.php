<?php

namespace App\Livewire;

use Livewire\Component;
use Illuminate\Support\Facades\Http;
use App\Services\ConversationApi;
use App\Models\Message;
use Livewire\WithPagination;
use App\Jobs\ProcessAssistantReply;

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

    public function getListeners(): array
    {
        // se esiste una chat attiva genero il canale, altrimenti niente listener
        return $this->activeConversation
            ? ["echo:conversations.{$this->activeConversation},MessageUpdated" => 'handleBroadcast']
            : [];
    }

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
    if ($this->isSending) return;
    $this->isSending = true;

    $content = trim($this->newMessage);
    if ($content === '' || ! $this->activeConversation) {
        $this->isSending = false;
        return;
    }

    $userId = auth()->id();   // o altro modo per ottenere lo user id corrente

    $userMsg = Message::create([
        'conversation_id' => $this->activeConversation,
        'user_id'         => $userId,        //  👈  necessario
        'content'         => $content,
        'sender'          => 'user',
    ]);

    $assistantMsg = Message::create([
        'conversation_id' => $this->activeConversation,
        'user_id'         => $userId,        // usa lo stesso owner della chat
        'content'         => 'Sto pensando…',
        'sender'          => 'assistant',
    ]);

    /* 3️⃣  Aggiorna la UI locale */
    $this->messages[] = $userMsg->toArray();
    $this->messages[] = $assistantMsg->toArray();
    $this->newMessage = '';

    /* 4️⃣  Dispatch del Job */
    ProcessAssistantReply::dispatch(
        $this->activeConversation,
        $assistantMsg->id,
        $content,
        userId: auth()->id(),
    );

    // ProcessAssistantReply::dispatch(
    //     conversationId: $conversation->id,
    //     assistantMessageId: $assistantMessage->id,
    //     prompt: $prompt,
    //     userId: auth()->id(),           // 👈 ora è valorizzato
    // );

    $this->isSending = false;
}


    public function getMessagesProperty()
    {
        return Message::where('conversation_id', $this->activeConversation)
        // ->where('id', '<=', $this->lastSeenId)  // $lastSeenId = id più alto già caricato
        ->orderByDesc('id')          // ① prendi gli ultimi (id più alti)
        ->take($this->perPage)       // ② limitali a N = $perPage
        ->get()
        ->reverse();                // ③ inverti per mostrarli dal più vecchio al più nuovo
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

    public function handleBroadcast($payload)
    {
        // aggiorna l’array $messages o fai refresh
        $this->refreshMessages();
    }
}
