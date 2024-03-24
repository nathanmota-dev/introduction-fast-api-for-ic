CREATE TABLE message (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    content VARCHAR NOT NULL,
    published BOOLEAN DEFAULT true,
    created_at TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE public.message (
    id SERIAL PRIMARY KEY,
    title character varying NOT NULL,
    content character varying NOT NULL,
    published BOOLEAN DEFAULT True,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT now()
);

ALTER TABLE IF EXISTS public.message
    OWNER TO postgres;
	
INSERT INTO public.message (title, content)
VALUES 
('Título 1', 'Conteúdo da mensagem 1'),
('Título 2', 'Conteúdo da mensagem 2'),
('Título 3', 'Conteúdo da mensagem 3');
