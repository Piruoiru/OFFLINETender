<?php

namespace App\Http\Controllers;

use App\Models\Conversation;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Http;
use App\Repositories\Contracts\MessageRepositoryInterface;

class MessageController extends Controller
{
    protected MessageRepositoryInterface $messageRepository;

    public function __construct(MessageRepositoryInterface $messageRepository)
    {
        $this->messageRepository = $messageRepository;
    }

    /** GET /api/conversations/{conversation}/messages */
    public function index(Conversation $conversation)
    {
        // Ordinati dal più vecchio al più nuovo
        return $conversation->messages()->oldest()->paginate(20);
    }

    /** POST /api/conversations/{conversation}/messages */
    public function storeMessage(Request $request, Conversation $conversation)
    {   
        // logger()->info('⚠️ storeMessage called', $request->all());

        // ⬅️ NB: validiamo solo "content" e "sender=user"
        $data = $request->validate([
            'content' => 'required|string',
            'sender'  => 'required|in:user',
        ]);

        /* 1️⃣ Salva il messaggio dell’utente e lo teniamo in $userMessage */
        $userMessage = $this->messageRepository->store($conversation, [
            'user_id' => $request->user_id,        // sempre l’utente loggato
            'content' => $data['content'],
            'sender'  => 'user',
        ]);

        /* 2️⃣ Chiediamo la risposta al modello LLM (sincrono, come prima) */
        $reply = '[errore: nessuna risposta]';
        try {
            $response = Http::baseUrl(config('services.llm.url'))
                ->timeout(3600)
                ->post('/chat', [
                    'conversation_id' => $conversation->id,
                    'message'         => $data['content'],
                ])
                ->throw();

            $reply = $response->json('response', $reply)
                   ?: '[errore: JSON senza campo "response"]';
        } catch (\Throwable $e) {
            logger()->error('LLM error', ['e' => $e]);
        }

        /* 3️⃣ Salva la risposta dell’assistente (ma NON la restituiamo) */
        $this->messageRepository->store($conversation, [
            'user_id' => $request->user_id,
            'sender'  => 'assistant',
            'content' => $reply,
        ]);

        /* 4️⃣ Risponde 201 + JSON con **solo** il record utente */
        return response()->json($userMessage, 201);
    }
}
