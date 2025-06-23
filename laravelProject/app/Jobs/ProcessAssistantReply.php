<?php

namespace App\Jobs;

use App\Models\Message;
use App\Services\ConversationApi;
use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use App\Events\MessageUpdated;
use Throwable;

class ProcessAssistantReply implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public function __construct(
        public int $conversationId,
        public int $assistantMessageId, // id della **riga placeholder** creata dal componente
        public string $prompt,          // testo dell’utente
        public int $userId
    ) {}

    public function handle(ConversationApi $api): void
    {
        // ① prendi la riga placeholder
        $msg = Message::findOrFail($this->assistantMessageId);

        // ② chiedi la risposta al modello LLM (NON ricreare alcun messaggio)
        $answer = $api->askLLM($this->conversationId, $this->prompt);

        // ③ sovrascrivi il contenuto della riga assistant
        $msg->update([
            'content' => $answer ?: '🤖 (vuoto)',
        ]);

        // ④ notifica il front-end
        broadcast(new MessageUpdated($msg));
    }

    public function failed(Throwable $e): void
    {
        Message::find($this->assistantMessageId)?->update([
            'content' => '❌ Errore: '.$e->getMessage(),
        ]);
    }

    public function prioritize(): string
    {
        return 'medium';
    }
}
