<?php

namespace App\Http\Controllers;

use App\Models\{Conversation, Message};
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\StreamedResponse;

class MessageStreamController
{
    /**
     * GET /api/conversations/{conversation}/stream
     * Server-Sent Events che pushano ogni nuovo messaggio.
     * Il client può (opzionale) inviare Last-Event-ID per riprendere.
     */
    public function __invoke(Request $request, Conversation $conversation): StreamedResponse
    {
        // l’utente deve possedere la conversazione
        auth()->user()->can('view', $conversation) || abort(403);

        // se Last-Event-ID non c’è partiamo da 0
        $lastId = (int) $request->header('Last-Event-ID', 0);

        return response()->stream(function () use ($conversation, &$lastId) {
            while (true) {
                $new = Message::where('conversation_id', $conversation->id)
                              ->where('id', '>', $lastId)
                              ->orderBy('id')
                              ->get();

                foreach ($new as $msg) {
                    echo "id: {$msg->id}\n";
                    echo "event: {$msg->sender}\n";
                    echo "data: ".json_encode($msg)."\n\n";
                    $lastId = $msg->id;
                }

                // flush buffer
                ob_flush();
                flush();
                usleep(350_000); // 0.35 s
            }
        }, 200, [
            'Content-Type'      => 'text/event-stream',
            'Cache-Control'     => 'no-cache',
            'X-Accel-Buffering' => 'no',
            'Connection'        => 'keep-alive',
        ]);
    }
}
