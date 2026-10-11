"""Genera las páginas internas de Axis Legal (comparten head, header, menú, footer y flotantes).
Correr de nuevo después de cualquier cambio de estructura; el CSS va en styles.css."""
import json, os
D = r"C:\Users\axeli\Desktop\laburo\Desarrollo Web\bocetos-estudios\Axis Legal"
os.chdir(D)

WA_DEF = "Hola, quisiera hacer una consulta."
PX = {  # fotos de Pexels (registro para no repetirlas en otros proyectos)
  "sucesiones": 36758296, "penal": 6006866, "laboral": 29083058, "transito": 10410202, "amparos": 28987495,
  "comercial": 8371735, "inmobiliario": 26547201, "estudio": 36207461, "biblioteca": 37165246,
}
def px_comment(key):
    i = PX[key]
    return f"<!-- foto de fondo: https://images.pexels.com/photos/{i}/pexels-photo-{i}.jpeg -->"

# ------------------------------------------------------------------ preguntas (todas, por área)
FAQ = {
 "sucesiones": [
  ("¿Qué es el proceso sucesorio y cuándo conviene iniciarlo?", "Es el trámite judicial que determina quiénes son los herederos y les transmite los bienes de la persona fallecida. Conviene iniciarlo cuanto antes: mientras no se abre, los bienes no pueden venderse ni ponerse a nombre de los herederos, y con el tiempo se vuelve más difícil reunir la documentación."),
  ("¿Cuánto tiempo lleva y cuánto cuesta una sucesión?", "Depende de la jurisdicción, de la cantidad de herederos y de si hay acuerdo entre ellos. Una sucesión sin conflictos se resuelve antes que una con bienes en varias provincias o con desacuerdos. Después de la primera entrevista te pasamos por escrito los honorarios y los gastos previsibles, en 24 a 48 h hábiles."),
  ("¿Qué sucede si la persona falleció sin testamento?", "La ley define quiénes heredan y en qué orden: primero los hijos y demás descendientes junto con el cónyuge; si no los hay, los padres y demás ascendientes junto con el cónyuge; luego el cónyuge solo, y por último los parientes colaterales hasta el cuarto grado. El juez lo reconoce en la declaratoria de herederos."),
  ("¿Quiénes son los herederos forzosos y qué es la legítima?", "Son los descendientes, los ascendientes y el cónyuge. La legítima es la porción de la herencia que la ley les reserva y de la que no se los puede privar, ni siquiera por testamento: dos tercios para los descendientes y la mitad para los ascendientes o el cónyuge."),
  ("¿Puedo vender un inmueble heredado antes de finalizar la sucesión?", "Para escriturar a nombre de un comprador, en general la sucesión tiene que haber llegado al menos a la declaratoria de herederos. Hay alternativas, como la venta por tracto abreviado o la cesión de derechos hereditarios, que permiten adelantar la operación. Analizamos cuál conviene en tu caso."),
  ("¿Qué documentación necesito para iniciar el trámite?", "Habitualmente: la partida de defunción, las partidas que acreditan el vínculo de los herederos (nacimiento, matrimonio), el DNI de los interesados, la documentación de los bienes (escrituras, datos de vehículos y cuentas) y el testamento, si existe. En la primera entrevista te decimos qué falta y lo gestionamos con vos."),
  ("¿Las deudas del fallecido también se heredan?", "Los herederos no responden con su propio patrimonio: las deudas se pagan con los bienes de la herencia y, en general, cada heredero responde solo hasta el valor de lo que recibe. Por eso conviene conocer las deudas antes de tomar decisiones."),
  ("¿Se puede renunciar a una herencia?", "Sí, mientras no se la haya aceptado. La renuncia se hace por escritura pública o por acta ante el juzgado de la sucesión, y quien renuncia queda como si nunca hubiera sido heredero. Antes de hacerlo, conviene evaluar las consecuencias para el resto de la familia."),
 ],
 "derecho-penal": [
  ("Recibí una citación o notificación judicial, ¿qué debo hacer?", "No la ignores ni te presentes sin asesoramiento. Fijate qué organismo la emite, la fecha y el motivo, y consultanos con la notificación en mano: revisamos la causa, preparamos la declaración y te acompañamos al acto."),
  ("¿Cómo realizo una denuncia penal?", "Se puede presentar en una comisaría o ante la fiscalía, y en muchas jurisdicciones también por medios electrónicos. Conviene hacerla con asesoramiento: una denuncia clara, con los hechos ordenados y la prueba disponible, facilita la investigación. Podemos redactarla y presentarla por vos."),
  ("¿Qué derechos tengo si soy detenido?", "Tenés derecho a saber por qué se te detiene, a no declarar contra vos mismo, a comunicarte con un familiar y a ser asistido por un abogado de tu confianza antes de declarar. Lo más importante: no declares sin un defensor presente."),
  ("¿Qué es la suspensión del proceso a prueba (probation)?", "Es una salida alternativa al juicio para ciertos delitos: la causa se suspende por un plazo durante el cual la persona cumple reglas de conducta y ofrece una reparación del daño. Si las cumple, la acción penal se extingue y no queda condena."),
  ("¿Qué diferencia hay entre denunciante y querellante?", "El denunciante solo pone el hecho en conocimiento de las autoridades. El querellante, en cambio, es parte en el proceso: puede proponer prueba, intervenir en las audiencias y recurrir decisiones. La víctima puede constituirse como querellante con el patrocinio de un abogado."),
 ],
 "derecho-laboral": [
  ("Me despidieron, ¿qué pasos debo seguir?", "No firmes nada que no entiendas y guardá los recibos de sueldo, los telegramas y cualquier comunicación. Revisá si el despido fue con o sin causa y si la liquidación final está bien calculada. Consultanos pronto: los plazos para intimar y reclamar son cortos."),
  ("¿Cómo se calcula la indemnización por despido sin causa?", "En general incluye un mes de la mejor remuneración mensual por cada año trabajado (o fracción mayor de tres meses), el preaviso si no se otorgó, la integración del mes de despido y los proporcionales de aguinaldo y vacaciones. Cada caso tiene particularidades: hacemos el cálculo con tus recibos."),
  ("Trabajo sin estar registrado (\u00aben negro\u00bb), ¿qué puedo reclamar?", "Podés intimar a tu empleador para que registre la relación laboral con la fecha de ingreso y el salario reales, y reclamar las diferencias salariales, los aportes y, si la relación termina, la indemnización que corresponda. Las reglas cambiaron en los últimos años, así que conviene analizar tu caso con la normativa vigente."),
  ("¿Cuánto tiempo tengo para reclamar?", "Como regla general, los créditos laborales prescriben a los dos años. Pero algunas intimaciones tienen plazos mucho más cortos, de días, así que lo mejor es consultar apenas surge el conflicto."),
  ("¿Qué es el telegrama laboral y cuándo se envía?", "Es una comunicación fehaciente entre trabajador y empleador: deja constancia de una intimación, un despido o una renuncia. Su redacción es decisiva, porque lo que se dice (y lo que no) puede condicionar todo el reclamo posterior. Te ayudamos a redactarlo."),
 ],
 "accidentes-de-transito": [
  ("¿Qué debo hacer si tuve un accidente de tránsito?", "Si hay heridos, pedí asistencia médica. Sacá fotos del lugar y de los vehículos, anotá los datos del otro conductor, su patente y su seguro, y buscá testigos. Hacé la denuncia del siniestro ante tu aseguradora dentro de los tres días y guardá toda la documentación médica."),
  ("¿Necesito abogado para hacer el reclamo?", "No es obligatorio para reclamar ante la aseguradora, pero sí recomendable: un abogado sabe qué rubros reclamar, cómo acreditar el daño y cuándo una oferta es baja. Si hay que ir a juicio, el patrocinio letrado es necesario."),
  ("¿Qué puedo reclamar después de un accidente?", "Según el caso: los daños del vehículo, los gastos médicos y de traslado, la incapacidad física o psicológica, los días de trabajo perdidos, la privación del uso del vehículo y el daño moral."),
  ("¿Cuánto tiempo tengo para reclamar?", "En general, el plazo para reclamarle al responsable es de tres años desde el accidente. Algunos plazos frente a las aseguradoras son más cortos, por eso conviene consultar cuanto antes."),
  ("¿Cuánto tarda un reclamo por accidente?", "Si se llega a un acuerdo con la aseguradora, puede resolverse en meses. Si hace falta un juicio, el proceso es más largo y depende de la prueba y del juzgado. Te mantenemos informado de cada avance."),
  ("¿Qué pasa si el otro conductor no tiene seguro?", "Igual se puede reclamar: la acción se dirige contra el conductor y el titular del vehículo, que responden con su patrimonio. Analizamos su solvencia para definir la mejor estrategia."),
  ("¿Puedo reclamar si fui acompañante o peatón?", "Sí. Los acompañantes y los peatones son terceros damnificados y pueden reclamar los daños sufridos al responsable del accidente y a su aseguradora."),
 ],
 "amparos-de-salud": [
  ("¿Qué es un amparo de salud?", "Es una acción judicial rápida para proteger el derecho a la salud cuando una obra social o una prepaga niega, demora o limita una cobertura médica necesaria."),
  ("¿Cuándo conviene iniciar un amparo?", "Cuando hay una negativa o una demora injustificada y la prestación es necesaria según tu médico. Si la situación es urgente, no conviene esperar: el amparo permite pedir una medida cautelar de inmediato."),
  ("¿Qué documentación se necesita?", "La prescripción y el resumen de historia clínica firmados por el médico, la negativa de la obra social o la prepaga (o la constancia del pedido sin respuesta), tu credencial y, si corresponde, los comprobantes de pago de la cuota."),
  ("¿Cuánto tarda un amparo de salud?", "Cuando hay urgencia, la medida cautelar puede resolverse en pocos días. La sentencia definitiva lleva más tiempo, pero mientras tanto la cautelar asegura la prestación."),
  ("¿Qué puede ordenarse en un amparo?", "El juez puede ordenar la cobertura total o parcial de tratamientos, medicamentos, cirugías, internaciones, prótesis o acompañantes terapéuticos, según lo que el caso acredite."),
 ],
 "derecho-comercial": [
  ("¿Qué es el registro de marca?", "Es el trámite ante el INPI que te da el derecho exclusivo a usar un nombre, un logo o un signo para identificar tus productos o servicios. El registro dura diez años y se puede renovar."),
  ("¿Por qué conviene registrar una marca?", "Porque sin registro no tenés exclusividad: otro podría registrarla antes y hasta impedirte usarla. Además, una marca registrada es un activo de la empresa que se puede licenciar o vender."),
  ("¿Cuánto tarda el registro de marca?", "Depende de los plazos del INPI y de si hay oposiciones de terceros; en general lleva varios meses. Antes de presentarla hacemos una búsqueda de antecedentes para reducir riesgos."),
  ("¿Qué se necesita para registrar una marca?", "Los datos del titular, el nombre o el logo a registrar y las clases de productos o servicios que va a proteger. Te asesoramos en la elección de las clases, que es clave para que la protección sea útil."),
  ("¿Qué es la constitución de una sociedad?", "Es el proceso para crear una persona jurídica distinta de sus socios: se redacta el estatuto, se definen el capital y la administración, y se inscribe ante el organismo de control (en CABA, la IGJ)."),
  ("¿Qué tipo de sociedad conviene?", "Depende de la cantidad de socios, el capital, la actividad y los planes de crecimiento. Las más usuales son la SAS, la SRL y la SA; analizamos tu proyecto para recomendarte la más adecuada."),
  ("¿Cuánto tarda constituir una sociedad?", "Varía según el tipo societario y el organismo de inscripción. Las SAS suelen ser las más ágiles; una SRL o una SA requieren algo más de tiempo. Te damos un plazo estimado al empezar."),
 ],
 "derecho-inmobiliario": [
  ("¿Qué es el boleto de compraventa?", "Es el contrato previo a la escritura en el que comprador y vendedor fijan el precio, la forma de pago, la fecha de escrituración y la entrega del inmueble. Lo que se firma en el boleto condiciona toda la operación.", "Compraventa"),
  ("¿Qué informes deben pedirse antes de comprar un inmueble?", "Como mínimo, el informe de dominio, el de inhibiciones del vendedor y los certificados de deuda de impuestos, servicios y expensas. Revisarlos antes de firmar evita sorpresas en la escritura.", "Compraventa"),
  ("¿Quién elige al escribano y qué gastos implica la operación?", "Por costumbre lo elige el comprador, salvo acuerdo en contrario. Los gastos incluyen los honorarios notariales, los impuestos y los certificados, y se reparten entre las partes según lo pactado y la jurisdicción.", "Compraventa"),
  ("¿Qué debe contener un contrato de alquiler bien redactado?", "Plazo, precio y forma de actualización, garantías, depósito, quién paga expensas e impuestos, estado del inmueble y condiciones de rescisión. Cuanto más claro es el contrato, menos conflictos hay.", "Alquileres"),
  ("¿Cómo se actualiza el precio del alquiler?", "Desde la derogación de la ley de alquileres, a fines de 2023, las partes acuerdan libremente el índice y la periodicidad de la actualización. Por eso es clave dejarlo bien definido en el contrato.", "Alquileres"),
  ("¿Qué puedo hacer si el inquilino no paga?", "El primer paso es intimarlo formalmente al pago. Si no regulariza, se puede iniciar el juicio de desalojo junto con el reclamo de los alquileres adeudados contra el inquilino y sus garantes.", "Alquileres"),
  ("¿Puedo donar un inmueble a un hijo u otro familiar?", "Sí. La donación a un hijo se considera un adelanto de su herencia, lo que puede tener efectos en la sucesión futura. Conviene planificarla para proteger a toda la familia.", "Donaciones"),
  ("¿Qué costos e impuestos tiene una donación?", "Los honorarios del escribano y, según la jurisdicción, impuestos como el de sellos o, en Provincia de Buenos Aires, el impuesto a la transmisión gratuita de bienes. Los calculamos antes de avanzar.", "Donaciones"),
  ("¿Qué es el usufructo y cómo se constituye?", "Es el derecho a usar un bien ajeno y percibir sus frutos sin alterar su sustancia. Sobre inmuebles se constituye por escritura pública; es habitual en donaciones de padres a hijos con reserva de usufructo.", "Usufructo"),
  ("¿Qué derechos tiene el cónyuge supérstite sobre la vivienda?", "Puede tener un derecho real de habitación gratuito y vitalicio sobre el inmueble que fue la última residencia familiar, si en ese momento no estaba en condominio con otras personas.", "Usufructo"),
  ("¿Qué es la cesión de derechos hereditarios?", "Es el contrato por el que un heredero transfiere, total o parcialmente, sus derechos sobre una herencia. Se hace por escritura pública y permite adelantar operaciones sin esperar el final de la sucesión.", "Cesiones de derechos"),
  ("¿Qué son los derechos posesorios y pueden cederse?", "Son los derechos de quien posee un inmueble sin tener un título inscripto a su nombre. Pueden cederse, pero la operación tiene riesgos: requiere un análisis dominial cuidadoso antes de pagar.", "Cesiones de derechos"),
  ("¿Qué es un fideicomiso inmobiliario?", "Es una estructura en la que los inversores aportan fondos a un fiduciario que administra la construcción y después entrega las unidades. Es habitual en las compras de departamentos en pozo.", "Fideicomisos"),
  ("¿Qué garantías tengo al comprar dentro de un fideicomiso?", "Depende del contrato. Antes de que inviertas revisamos quiénes son el fiduciario y el desarrollador, la titularidad del terreno, el permiso de obra, el cronograma y las cláusulas ante incumplimientos.", "Fideicomisos"),
 ],
}

# ------------------------------------------------------------------ áreas
AREAS = [
 dict(slug="sucesiones", n="01", name="Sucesiones", img="sucesiones", pos="center 40%", principal=True,
  title="Abogados de sucesiones en CABA y Provincia de Buenos Aires | Axis Legal",
  desc="Tramitación integral de sucesiones en CABA y Provincia de Buenos Aires: declaratoria de herederos, testamentos, transmisión de bienes y cesión de derechos. Respuesta en menos de 24 h.",
  h1=("Sucesiones,", "con claridad en cada etapa."),
  lead="Acompañamos a herederos y familias de CABA y Provincia de Buenos Aires en todo el trámite sucesorio: desde la documentación inicial hasta la inscripción de los bienes a su nombre.",
  msg="Hola, quisiera consultar por una sucesión.",
  sobre_h2=("¿Qué es", "una sucesión?"),
  sobre=["Es el proceso por el cual, al fallecer una persona, sus bienes, derechos y obligaciones pasan a sus herederos. Cuando hay patrimonio para transmitir, ese traspaso se formaliza con un trámite judicial.",
         "La sucesión identifica a los herederos, reúne y valúa los bienes y obtiene la autorización del juez para inscribirlos a su nombre o disponer de ellos. Sin ella no se puede vender, escriturar ni administrar formalmente lo heredado.",
         "Te explicamos cada etapa sin tecnicismos y adaptamos la estrategia a la situación de tu familia."],
  serv=[("ti-scale", "Sucesiones intestadas", "Sin testamento, la ley define quiénes heredan y en qué proporción. Tramitamos la declaratoria ante el juzgado competente."),
        ("ti-writing", "Sucesiones testamentarias", "Validamos el testamento y transmitimos los bienes según la voluntad del causante, respetando la legítima de los herederos forzosos."),
        ("ti-certificate", "Declaratoria de herederos", "La resolución que reconoce a los herederos y los habilita a administrar y disponer de los bienes."),
        ("ti-home", "Transmisión de bienes", "Alternativas para liquidar, dividir y adjudicar inmuebles, vehículos, cuentas y demás bienes de la herencia."),
        ("ti-arrows-exchange", "Cesión de derechos hereditarios", "Orientación sobre la cesión de derechos y sobre las obligaciones de cada heredero."),
        ("ti-shield-check", "Planificación patrimonial", "Testamentos y decisiones en vida para ordenar la transmisión del patrimonio y evitar conflictos futuros.")],
  pasos=[("Consulta y análisis inicial", "Revisamos la situación familiar y patrimonial, los herederos y la documentación disponible."),
         ("Reunión de la documentación", "Gestionamos los certificados y las partidas que falten para iniciar el trámite."),
         ("Inicio del trámite", "Definimos la vía sucesoria e iniciamos la sucesión ante el juzgado competente."),
         ("Seguimiento hasta el final", "Acompañamos el proceso hasta la inscripción o la disposición de los bienes.")],
  docs=["Partida o certificado de defunción.", "Partidas que acrediten el vínculo de los herederos (nacimiento, matrimonio).",
        "DNI de los interesados en la sucesión.", "Documentación de los bienes: escrituras, datos registrales, vehículos y cuentas.",
        "Testamento, si existe.", "Otra documentación que pidamos según las circunstancias del caso."],
  faq=[0, 1, 4, 5]),
 dict(slug="derecho-penal", n="02", name="Derecho penal", img="penal", pos="center 30%",
  title="Abogados penalistas en CABA | Defensa penal y querellas | Axis Legal",
  desc="Defensa penal y representación de víctimas en CABA y Gran Buenos Aires. Citaciones, denuncias, querellas, probation y excarcelaciones, desde la primera etapa del proceso.",
  h1=("Derecho penal,", "defensa desde el primer momento."),
  lead="Defensa de personas imputadas y representación de víctimas. Intervenimos desde la primera citación, con una estrategia clara y comunicación permanente.",
  msg="Hola, quisiera consultar por una causa penal.",
  sobre_h2=("Actuar rápido", "marca el rumbo."),
  sobre=["Tanto si estás imputado como si fuiste víctima de un delito, te acompañamos en cada etapa del proceso.",
         "En materia penal los plazos corren igual, y las decisiones de las primeras horas definen el rumbo de toda la causa. Por eso analizamos la imputación o el hecho denunciado de inmediato y con rigor."],
  serv=[("ti-shield", "Defensa penal", "Representación de personas imputadas desde la primera declaración hasta el juicio."),
        ("ti-gavel", "Querella de víctimas", "Constitución como querellante para impulsar la causa y ofrecer prueba."),
        ("ti-mail-opened", "Citaciones y notificaciones", "Asesoramiento ante citaciones policiales o judiciales y preparación de la declaración."),
        ("ti-hourglass", "Suspensión del proceso a prueba", "Gestión de la probation y de otras salidas alternativas al juicio."),
        ("ti-lock-open", "Excarcelación", "Pedidos de libertad y revisión de la situación procesal."),
        ("ti-file-alert", "Denuncias penales", "Redacción y presentación de denuncias, con seguimiento de la causa.")],
  pasos=[("Consulta urgente", "Analizamos la imputación, la citación o el hecho denunciado."),
         ("Estrategia", "Definimos el abordaje procesal y preparamos la declaración o la denuncia."),
         ("Intervención", "Te asistimos en la audiencia y en cada acto procesal."),
         ("Seguimiento", "Monitoreamos la causa y te mantenemos informado en cada etapa.")],
  faq=[0, 1, 2, 3]),
 dict(slug="derecho-laboral", n="03", name="Derecho laboral", img="laboral", pos="center 35%",
  title="Abogados laborales en CABA | Despidos e indemnizaciones | Axis Legal",
  desc="Asesoramiento laboral para trabajadores y empleadores en CABA y Gran Buenos Aires: despidos, indemnizaciones, trabajo no registrado, accidentes de trabajo y telegramas.",
  h1=("Derecho laboral,", "tus derechos en el trabajo."),
  lead="Asesoramiento a trabajadores y empleadores en despidos, indemnizaciones, trabajo no registrado, accidentes de trabajo y conflictos laborales en general.",
  msg="Hola, quisiera consultar por un tema laboral.",
  sobre_h2=("Plazos cortos,", "trámites precisos."),
  sobre=["En derecho laboral los plazos son cortos y las comunicaciones tienen que ser fehacientes: conviene consultar apenas surge el conflicto.",
         "Redactamos telegramas con precisión, calculamos indemnizaciones según la normativa vigente y patrocinamos reclamos administrativos y judiciales. También acompañamos a empleadores en desvinculaciones y conflictos con el personal."],
  serv=[("ti-briefcase-off", "Despidos e indemnizaciones", "Cálculo y reclamo de la indemnización por despido sin causa y de las diferencias adeudadas."),
        ("ti-file-off", "Trabajo no registrado", "Reclamos por falta de registración o registración deficiente de la relación laboral."),
        ("ti-first-aid-kit", "Accidentes de trabajo", "Reclamos ante la ART y demandas por incumplimientos de la normativa."),
        ("ti-cash", "Diferencias salariales", "Reclamo de diferencias por categoría, horas extras y conceptos no abonados."),
        ("ti-send", "Telegramas laborales", "Redacción precisa de intimaciones y comunicaciones fehacientes."),
        ("ti-building", "Asesoramiento a empleadores", "Desvinculaciones, conflictos y cumplimiento de la normativa laboral.")],
  pasos=[("Análisis del caso", "Revisamos la situación laboral y la documentación del trabajador o del empleador."),
         ("Intimación fehaciente", "Redactamos y enviamos el telegrama laboral con la redacción exacta."),
         ("Negociación", "Buscamos un acuerdo favorable antes de iniciar la demanda."),
         ("Reclamo judicial", "Si no hay acuerdo, patrocinamos el reclamo ante el fuero del trabajo.")],
  faq=[0, 1, 2, 3]),
 dict(slug="accidentes-de-transito", n="04", name="Accidentes de tránsito", img="transito", pos="center 55%",
  title="Abogados de accidentes de tránsito en CABA | Reclamos | Axis Legal",
  desc="Reclamos por lesiones y daños en accidentes de tránsito frente a aseguradoras y responsables, con seguimiento médico-legal. Acompañantes, peatones y conductores sin seguro.",
  h1=("Accidentes de tránsito,", "un reclamo integral."),
  lead="Reclamos por daños y lesiones derivados de siniestros viales, frente a aseguradoras y responsables civiles, con seguimiento médico-legal del caso.",
  msg="Hola, quisiera consultar por un accidente de tránsito.",
  sobre_h2=("El daño real,", "bien reclamado."),
  sobre=["El resultado de un reclamo depende de reunir la información correcta y de actuar dentro de los plazos legales.",
         "Acompañamos el caso con seguimiento médico-legal para que la indemnización refleje el daño real: lesiones, días de trabajo perdidos, gastos médicos y daño moral. También intervenimos cuando el otro conductor no tiene seguro o cuando el damnificado es acompañante o peatón."],
  serv=[("ti-heartbeat", "Indemnización por lesiones", "Reclamo por lesiones físicas, secuelas y daño moral tras el siniestro."),
        ("ti-car-crash", "Daños materiales", "Reclamo por los daños del vehículo y de los bienes afectados."),
        ("ti-file-certificate", "Reclamos ante aseguradoras", "Gestión del reclamo administrativo y negociación con la aseguradora."),
        ("ti-alert-triangle", "Conductor sin seguro", "Reclamo directo contra el responsable civil cuando no hay cobertura."),
        ("ti-walk", "Acompañantes y peatones", "Reclamos de terceros damnificados en el siniestro."),
        ("ti-stethoscope", "Seguimiento médico-legal", "Acompañamiento de la evolución clínica para cuantificar el daño.")],
  pasos=[("Reunión de información", "Recopilamos fotos, datos del otro vehículo, la póliza y la denuncia del siniestro."),
         ("Evaluación del daño", "Analizamos las lesiones, los gastos y los días de trabajo perdidos."),
         ("Reclamo a la aseguradora", "Presentamos el reclamo y negociamos una indemnización completa."),
         ("Demanda judicial", "Si la aseguradora no da una respuesta adecuada, iniciamos la demanda.")],
  faq=[0, 1, 2, 3]),
 dict(slug="amparos-de-salud", n="05", name="Amparos de salud", img="amparos", pos="center 50%",
  title="Amparos de salud en CABA | Obras sociales y prepagas | Axis Legal",
  desc="Amparos de salud frente a negativas o demoras de obras sociales y prepagas: tratamientos, medicamentos, cirugías y medidas cautelares urgentes en CABA y Gran Buenos Aires.",
  h1=("Amparos de salud,", "tu derecho a la cobertura."),
  lead="Asesoramiento y representación frente a demoras, negativas o incumplimientos de obras sociales, prepagas y otros agentes del sistema de salud.",
  msg="Hola, quisiera consultar por un amparo de salud.",
  sobre_h2=("Una acción rápida", "para lo urgente."),
  sobre=["Intervenimos cuando una obra social o una prepaga niega o demora una cobertura médica necesaria. El amparo de salud es una acción judicial rápida que protege el derecho constitucional a la salud.",
         "No hace falta esperar meses: con la documentación médica y la negativa de la cobertura se puede presentar el amparo y, en casos urgentes, pedir una medida cautelar que ordene la prestación mientras el juicio avanza."],
  serv=[("ti-clipboard-heart", "Cobertura de tratamientos", "Reclamo de cobertura de tratamientos, estudios y prácticas médicas."),
        ("ti-pill", "Medicamentos", "Reclamo de cobertura de medicamentos de alto costo o no incluidos."),
        ("ti-building-hospital", "Cirugías e internaciones", "Gestión judicial de cirugías e internaciones negadas o demoradas."),
        ("ti-users", "Acompañantes terapéuticos", "Reclamo de cobertura de acompañantes terapéuticos y de enfermería."),
        ("ti-bolt", "Medidas cautelares", "Pedido de cobertura urgente mientras se tramita el amparo."),
        ("ti-id-badge-2", "Obras sociales y prepagas", "Reclamos frente a cualquier agente del sistema de salud.")],
  pasos=[("Reunión de documentación", "Historia clínica, prescripción médica y negativa de la obra social o la prepaga."),
         ("Evaluación", "Analizamos la urgencia y la viabilidad del amparo."),
         ("Presentación", "Iniciamos el amparo y, si corresponde, pedimos una medida cautelar."),
         ("Seguimiento", "Acompañamos el cumplimiento de la orden judicial y de la prestación.")],
  faq=[0, 1, 2, 3]),
 dict(slug="derecho-comercial", n="06", name="Derecho comercial", img="comercial", pos="center 40%",
  title="Abogados de derecho comercial en CABA | Sociedades, marcas y contratos | Axis Legal",
  desc="Asesoramiento comercial para empresas, comerciantes y emprendedores: constitución de sociedades, registro de marcas, contratos, conflictos societarios y cobro de deudas.",
  h1=("Derecho comercial,", "respaldo para tu empresa."),
  lead="Asesoramiento jurídico para empresas, comerciantes y emprendimientos en contratos, sociedades, conflictos comerciales y decisiones del día a día.",
  msg="Hola, quisiera consultar por un tema comercial.",
  sobre_h2=("Prevenir cuesta menos", "que litigar."),
  sobre=["Una buena planificación jurídica previene conflictos y protege tu inversión.",
         "Desde la constitución de una sociedad hasta el registro de una marca o la redacción de un contrato, cada trámite se hace con criterio y con la documentación necesaria para operar con seguridad."],
  serv=[("ti-registered", "Registro de marcas", "Trámite ante el INPI para proteger el nombre, el logo o el diseño de tu producto o servicio."),
        ("ti-building-skyscraper", "Constitución de sociedades", "Creación de SAS, SRL y SA con un estatuto a medida."),
        ("ti-file-text", "Contratos comerciales", "Redacción y revisión de contratos de suministro, distribución, locación y más."),
        ("ti-users-group", "Conflictos societarios", "Asesoramiento en disputas entre socios y resolución de conflictos."),
        ("ti-messages", "Asesoramiento del día a día", "Acompañamiento jurídico permanente para las decisiones comerciales."),
        ("ti-receipt", "Cobro de deudas", "Gestión y negociación del cobro de deudas comerciales.")],
  pasos=[("Consulta", "Analizamos tu proyecto, tu empresa o el conflicto comercial."),
         ("Plan", "Definimos la estructura societaria o el trámite más conveniente."),
         ("Gestión", "Hacemos el trámite ante el INPI o la IGJ, o redactamos los contratos."),
         ("Seguimiento", "Acompañamos la operatoria, las renovaciones y las actualizaciones.")],
  faq=[0, 1, 4, 5]),
 dict(slug="derecho-inmobiliario", n="07", name="Derecho inmobiliario", img="inmobiliario", pos="center 50%",
  title="Abogados inmobiliarios en CABA | Compraventa, alquileres y fideicomisos | Axis Legal",
  desc="Asesoramiento inmobiliario en CABA y Gran Buenos Aires: boleto de compraventa, alquileres y desalojos, donaciones, usufructo, cesiones de derechos y fideicomisos.",
  h1=("Derecho inmobiliario,", "operaciones con seguridad."),
  lead="Acompañamiento jurídico integral en operaciones inmobiliarias: compraventa, alquileres, donaciones, usufructo, cesiones de derechos y fideicomisos.",
  msg="Hola, quisiera consultar por una operación inmobiliaria.",
  sobre_h2=("Antes de firmar,", "verificamos todo."),
  sobre=["Revisamos la documentación antes de que firmes o entregues dinero.",
         "Un boleto bien redactado y los informes correctos previenen la mayoría de los conflictos. Por eso controlamos dominio, inhibiciones, deudas y situación registral, y coordinamos con el escribano para que la operación sea transparente."],
  serv=[("ti-key", "Compraventa y boleto", "Redacción del boleto y verificación de informes antes de la escritura."),
        ("ti-building-community", "Alquileres y desalojos", "Contratos a medida y juicios de desalojo con reclamo de alquileres adeudados."),
        ("ti-gift", "Donaciones de inmuebles", "Planificación patrimonial mediante donación, con análisis de costos e impuestos."),
        ("ti-home", "Usufructo y derechos reales", "Constitución de usufructo y planificación familiar del uso de los bienes."),
        ("ti-arrows-exchange", "Cesión de derechos posesorios", "Cesiones en inmuebles sin título inscripto, con análisis dominial riguroso."),
        ("ti-building-bank", "Fideicomisos inmobiliarios", "Revisión del contrato y del estado registral antes de invertir en pozo.")],
  pasos=[("Verificación", "Pedimos los informes de dominio, inhibiciones, deudas y situación registral."),
         ("Contrato", "Redactamos o revisamos el boleto o el contrato con cláusulas claras."),
         ("Escritura", "Coordinamos con el escribano y controlamos los requisitos para escriturar."),
         ("Inscripción", "Acompañamos la inscripción registral y la entrega del inmueble.")],
  faq=[0, 1, 3, 4]),
]

# ------------------------------------------------------------------ piezas compartidas
FONTS = "https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,300;0,400;0,600;0,700;1,400&family=Mulish:ital,wght@0,300;0,400;0,600;0,700;1,400&display=swap"
ORG = {"@type": "LegalService", "name": "Axis Legal", "telephone": "+54 9 11 5846-5239",
       "address": {"@type": "PostalAddress", "streetAddress": "Adolfo Alsina 1609, of. 26", "addressLocality": "Ciudad Autónoma de Buenos Aires", "addressCountry": "AR"},
       "openingHours": "Mo-Fr 10:00-17:00", "sameAs": ["https://www.instagram.com/estudiojuridico_axislegal"]}

def head(title, desc, ld=None, robots=None):
    ld_html = ""
    if ld:
        ld_html = '<script type="application/ld+json">\n' + json.dumps(ld, ensure_ascii=False, indent=2) + "\n</script>\n"
    rb = f'<meta name="robots" content="{robots}">\n' if robots else ""
    return f'''<!DOCTYPE html>
<html lang="es-AR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
{rb}<meta name="theme-color" content="#0B1710">
<link rel="icon" type="image/png" href="./favicon.png">
<link rel="apple-touch-icon" href="./favicon.png">
<meta property="og:type" content="website">
<meta property="og:locale" content="es_AR">
<meta property="og:site_name" content="Axis Legal">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{desc}">
<meta property="og:image" content="./og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="1200">
<meta name="twitter:card" content="summary">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="{FONTS}" rel="stylesheet">
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@tabler/icons-webfont@3.46.0/dist/tabler-icons.min.css">
<link rel="stylesheet" href="./styles.css">
{ld_html}</head>
<body>
'''

NAV = [("El estudio", "estudio.html"), ("Áreas", "index.html#areas"), ("Método", "index.html#metodo"),
       ("Preguntas", "preguntas-frecuentes.html"), ("Contacto", "index.html#contacto")]

CUR = ' aria-current="page"'

def header(active=None):
    def links():
        return "\n".join(f'      <a href="./{h}"{CUR if h == active else ""}>{t}</a>' for t, h in NAV)
    return f'''
<!-- ============ HEADER ============ -->
<header class="hdr" id="hdr">
  <div class="wrap hdr-in">
    <a href="./index.html" class="brand" aria-label="Axis Legal, inicio">
      <img src="./logo-claro.png" alt="Axis Legal" width="656" height="305">
    </a>
    <nav class="nav" aria-label="Principal">
{links()}
    </nav>
    <a class="btn btn-gold btn-sm hdr-cta js-wa" href="#" data-msg="{WA_DEF}">Consultar</a>
    <button class="burger" id="burger" aria-label="Abrir menú" aria-controls="mnav" aria-expanded="false"><span></span><span></span></button>
  </div>
</header>

<div class="mnav-ov" id="mnavOv"></div>
<nav class="mnav" id="mnav" aria-label="Menú">
  <img src="./logo-claro.png" alt="" class="mnav-logo" width="656" height="305">
{links().replace("      <a", "  <a")}
  <a class="btn btn-gold js-wa" href="#" data-msg="{WA_DEF}">Consultar por WhatsApp</a>
</nav>
'''

FOOTER = f'''
<!-- ============ FOOTER ============ -->
<footer class="ftr" id="ftr">
  <div class="wrap ftr-in">
    <div class="ftr-brand">
      <img src="./logo-claro.png" alt="Axis Legal" width="656" height="305" loading="lazy">
      <p>Asesoramiento legal integral en CABA y Gran Buenos Aires, con trato directo, honorarios claros y respuesta en menos de 24 horas.</p>
    </div>
    <div class="ftr-col">
      <h4>Estudio</h4>
      <ul>
        <li><a href="./estudio.html">El estudio</a></li>
        <li><a href="./index.html#metodo">Método</a></li>
        <li><a href="./preguntas-frecuentes.html">Preguntas frecuentes</a></li>
        <li><a href="./index.html#contacto">Contacto</a></li>
      </ul>
    </div>
    <div class="ftr-col">
      <h4>Áreas</h4>
      <ul>
{chr(10).join(f'        <li><a href="./{a["slug"]}.html">{a["name"]}</a></li>' for a in AREAS)}
      </ul>
    </div>
    <div class="ftr-col">
      <h4>Contacto</h4>
      <ul class="ftr-data">
        <li><i class="ti ti-brand-whatsapp"></i><a class="js-wa" href="#" data-msg="{WA_DEF}">11 5846-5239</a></li>
        <li><i class="ti ti-map-pin"></i><span>Adolfo Alsina 1609, of. 26, CABA</span></li>
        <li><i class="ti ti-clock"></i><span>Lun a vie, 10 a 17 h</span></li>
        <li><i class="ti ti-brand-instagram"></i><a href="https://www.instagram.com/estudiojuridico_axislegal" target="_blank" rel="noopener">@estudiojuridico_axislegal</a></li>
      </ul>
    </div>
  </div>
  <div class="ftr-bottom">
    <p>© <span id="yr">2026</span> Axis Legal. Todos los derechos reservados.</p>
    <p><a href="./privacidad.html">Política de privacidad</a></p>
    <p>Desarrollado por <a href="https://www.instagram.com/sageedev/" target="_blank" rel="noopener">@sageeDev</a></p>
  </div>
</footer>
'''

def tail(msg=WA_DEF):
    return f'''
<a class="wa-float js-wa" id="waFloat" href="#" data-msg="{msg}" aria-label="Escribir por WhatsApp"><i class="ti ti-brand-whatsapp"></i></a>

<script src="./main.js"></script>
</body>
</html>
'''

def crumbs(items):
    out = ['<li><a href="./index.html">Inicio</a></li>']
    for i, (t, h) in enumerate(items):
        if h:
            out.append(f'<li><i class="ti ti-chevron-right" aria-hidden="true"></i><a href="./{h}">{t}</a></li>')
        else:
            out.append(f'<li><i class="ti ti-chevron-right" aria-hidden="true"></i><span aria-current="page">{t}</span></li>')
    return '<nav aria-label="Ruta"><ol class="crumbs">' + "".join(out) + "</ol></nav>"

def page_hero(img, pos, crumb_items, h1, lead, ctas="", num=None, short=False, pxkey=None):
    bg = f'  <div class="ph-bg" aria-hidden="true" style="background-image:url(\'./img/{img}.jpg\');background-position:{pos}"></div>\n' if img else ""
    numh = f'  <span class="ph-num" aria-hidden="true">{num}</span>\n' if num else ""
    return f'''
<!-- ============ CABECERA ============ -->
{px_comment(pxkey) if pxkey else ""}
<section class="ph{' ph-short' if short else ''}">
{bg}{numh}  <div class="wrap ph-in">
    {crumbs(crumb_items)}
    <h1 class="ph-h1 split-words">{h1[0]} <em>{h1[1]}</em></h1>
    <p class="lead rise d2">{lead}</p>
{ctas}  </div>
</section>
'''

def faq_items(pairs):
    return "\n".join(f'      <li><details><summary><span>{q}</span><i class="ti ti-plus" aria-hidden="true"></i></summary><div class="faq-a"><p>{a}</p></div></details></li>' for q, a in pairs)

def cta_band(h2, lead, msg):
    return f'''
<!-- ============ CTA ============ -->
<section class="cta-band">
  <div class="cta-bg" aria-hidden="true"></div>
  <div class="wrap reveal">
    <h2 class="h2">{h2[0]} <em>{h2[1]}</em></h2>
    <p class="lead">{lead}</p>
    <div class="cta-ctas">
      <a class="btn btn-gold js-wa" href="#" data-msg="{msg}">Consultar por WhatsApp</a>
      <a class="btn btn-line" href="./index.html#contacto">Completar el formulario</a>
    </div>
    <ul class="cta-data">
      <li><i class="ti ti-map-pin"></i>Adolfo Alsina 1609, of. 26, CABA</li>
      <li><i class="ti ti-clock"></i>Lunes a viernes de 10 a 17 h</li>
    </ul>
  </div>
</section>
'''

def write(name, html):
    open(name, "w", encoding="utf8", newline="\n").write(html)
    print("ok", name)

# ------------------------------------------------------------------ páginas de área
for a in AREAS:
    slug = a["slug"]
    ctas = f'''    <div class="ph-ctas rise d3">
      <a class="btn btn-gold js-wa" href="#" data-msg="{a['msg']}">Consultar por WhatsApp</a>
      <a class="btn btn-line" href="./index.html#contacto">Completar el formulario</a>
    </div>
'''
    tag = '<p class="ph-tag rise">Área principal del estudio</p>\n' if a.get("principal") else ""
    hero = page_hero(a["img"], a["pos"], [("Áreas", "index.html#areas"), (a["name"], None)], a["h1"], a["lead"], ctas, num=a["n"], pxkey=a["img"])
    if tag:
        hero = hero.replace('    <h1 class="ph-h1', "    " + tag + '    <h1 class="ph-h1', 1)
    sobre_p = "\n".join(f"      <p>{p}</p>" for p in a["sobre"])
    serv = "\n".join(f'''      <li class="serv reveal"><i class="ti {ic}"></i><h3>{t}</h3><p>{d}</p></li>''' for ic, t, d in a["serv"])
    pasos = "\n".join(f'''      <li><span class="paso-n">{i+1}</span><h3>{t}</h3><p>{d}</p></li>''' for i, (t, d) in enumerate(a["pasos"]))
    docs = ""
    if a.get("docs"):
        docs_li = "\n".join(f'        <li><i class="ti ti-check"></i>{d}</li>' for d in a["docs"])
        docs = f'''
<!-- ============ DOCUMENTACIÓN ============ -->
<section class="docs">
  <div class="wrap docs-grid">
    <div class="reveal">
      <p class="eyebrow">Requisitos habituales</p>
      <h2 class="h2">Qué documentación <em>se necesita.</em></h2>
      <p class="lead">Es una lista orientativa: los requisitos varían según el caso y la jurisdicción. En la primera entrevista te decimos qué falta y lo gestionamos con vos.</p>
    </div>
    <ul class="docs-list reveal">
{docs_li}
    </ul>
  </div>
</section>
'''
    allq = FAQ[slug]
    pairs = [(allq[i][0], allq[i][1]) for i in a["faq"]]
    otras = "\n".join(f'      <a href="./{o["slug"]}.html">{o["name"]}</a>' for o in AREAS if o["slug"] != slug)
    lname = a["name"].lower() if slug != "accidentes-de-transito" else "accidentes de tránsito"
    ld = {"@context": "https://schema.org", "@type": "Service", "name": a["name"], "serviceType": a["name"],
          "areaServed": ["Ciudad Autónoma de Buenos Aires", "Provincia de Buenos Aires"], "provider": ORG}
    html = head(a["title"], a["desc"], ld) + header() + "\n<main>\n" + hero + f'''
<!-- ============ SOBRE EL ÁREA ============ -->
<section class="sobre">
  <div class="wrap sobre-grid">
    <div class="reveal">
      <p class="eyebrow">Sobre esta área</p>
      <h2 class="h2">{a['sobre_h2'][0]} <em>{a['sobre_h2'][1]}</em></h2>
    </div>
    <div class="sobre-txt reveal">
{sobre_p}
    </div>
  </div>
</section>

<!-- ============ SERVICIOS ============ -->
<section class="servicios">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Qué hacemos</p>
      <h2 class="h2">Servicios <em>del área.</em></h2>
    </div>
    <ul class="serv-grid">
{serv}
    </ul>
  </div>
</section>

<!-- ============ RECORRIDO ============ -->
<section class="recorrido">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Cómo trabajamos</p>
      <h2 class="h2">El recorrido <em>de tu caso.</em></h2>
    </div>
    <ol class="pasos reveal">
{pasos}
    </ol>
  </div>
</section>
{docs}
<!-- ============ PREGUNTAS ============ -->
<section class="faq">
  <div class="wrap faq-grid">
    <div class="reveal">
      <p class="eyebrow">Preguntas frecuentes</p>
      <h2 class="h2">Dudas habituales <em>sobre {lname}.</em></h2>
      <p class="lead">Si tu pregunta no está acá, escribinos y te responde un profesional del estudio.</p>
      <a href="./preguntas-frecuentes.html#{slug}" class="link-arrow">Ver todas las preguntas <i class="ti ti-arrow-right"></i></a>
    </div>
    <div class="reveal">
      <ul class="faq-list">
{faq_items(pairs)}
      </ul>
      <p class="faq-note">La información de este sitio es orientativa y no reemplaza el asesoramiento sobre tu caso.</p>
    </div>
  </div>
</section>

<!-- ============ OTRAS ÁREAS ============ -->
<section class="otras">
  <div class="wrap otras-in reveal">
    <h2>Otras áreas <em>del estudio</em></h2>
    <nav class="chips" aria-label="Otras áreas">
{otras}
    </nav>
  </div>
</section>
''' + cta_band(("¿Necesitás asesoramiento", f"en {lname}?"), "Cada consulta es confidencial y la responde un profesional del estudio, en menos de 24 horas hábiles.", a["msg"]) + "\n</main>\n" + FOOTER + tail(a["msg"])
    write(f"{slug}.html", html)

# ------------------------------------------------------------------ el estudio
METODO = [
 ("Primera entrevista", "Presencial en nuestro estudio de CABA o virtual, según prefieras. Escuchamos tu situación, revisamos la documentación que tengas y te damos un primer panorama. También te decimos qué más necesitamos para un análisis preciso."),
 ("Análisis integral del caso", "El equipo estudia la información reunida, evalúa las alternativas jurídicas y define en conjunto la estrategia. No buscamos respuestas apresuradas: le damos a tu caso el análisis que merece."),
 ("Presupuesto en 24 a 48 h hábiles", "Te enviamos por escrito los honorarios, los gastos previsibles y las formas de pago, para que decidas con información y sin sorpresas."),
 ("Inicio en 48 h hábiles", "Con tu confirmación y la documentación necesaria, coordinamos el inicio de las actuaciones: una demanda, un reclamo, una sucesión u otro trámite. Si algo modifica el cronograma, te avisamos."),
 ("Informe semanal", "Nuestra secretaría te envía cada semana, por email o WhatsApp, las actuaciones realizadas, las novedades del expediente, los próximos pasos y lo que necesitamos de vos."),
 ("Acompañamiento continuo", "El trabajo no termina con la presentación de un escrito. Te orientamos en cada etapa y te mantenemos al tanto de todo lo relevante hasta el final del proceso."),
]
eje = "\n".join(f'      <li class="reveal"><span class="eje-n">{i+1}</span><div><h3>{t}</h3><p>{d}</p></div></li>' for i, (t, d) in enumerate(METODO))
estudio = head("El estudio | Axis Legal, abogados en CABA y Gran Buenos Aires",
  "Más de veinte años de trayectoria y una generación formada en la gestión digital. Conocé el equipo, los compromisos y el método de trabajo de Axis Legal.",
  {"@context": "https://schema.org", **ORG, "foundingLocation": "Ciudad Autónoma de Buenos Aires"}) + header("estudio.html") + "\n<main>\n" + page_hero(
  "estudio", "center 45%", [("El estudio", None)], ("Soluciones jurídicas sólidas", "para casos que exigen más."),
  "Más de dos décadas de trayectoria, una mirada estratégica y herramientas de gestión modernas. Analizamos cada situación en profundidad y construimos la respuesta legal más conveniente para vos.",
  f'''    <div class="ph-ctas rise d3">
      <a class="btn btn-gold js-wa" href="#" data-msg="{WA_DEF}">Consultar por WhatsApp</a>
      <a class="btn btn-line" href="./index.html#areas">Ver las áreas</a>
    </div>
''', pxkey="estudio") + f'''
<!-- ============ INTRO + CIFRAS ============ -->
<section class="sobre">
  <div class="wrap">
    <div class="sobre-grid">
      <div class="reveal">
        <p class="eyebrow">Quiénes somos</p>
        <h2 class="h2">Estrategia, experiencia <em>y precisión.</em></h2>
      </div>
      <div class="sobre-txt reveal">
        <p>Somos un equipo interdisciplinario de abogados que combina trayectoria, solidez técnica y una mirada moderna del ejercicio profesional.</p>
        <p>Intervenimos en sucesiones, derecho penal, laboral, accidentes de tránsito, amparos de salud, comercial e inmobiliario, con criterio, precisión y un seguimiento cercano de principio a fin.</p>
      </div>
    </div>
    <ul class="cifras cifras-sep reveal" aria-label="El estudio en cifras">
      <li><b><span class="count" data-to="20" data-prefix="+">+20</span></b><small>años de trayectoria</small></li>
      <li><b><span class="count" data-to="7">7</span></b><small>áreas de práctica</small></li>
      <li><b><span class="count" data-to="24">24</span><i>h</i></b><small>para responder tu consulta</small></li>
      <li><b><span class="count" data-to="48">48</span><i>h</i></b><small>para iniciar tu caso</small></li>
    </ul>
  </div>
</section>

<!-- ============ COMPROMISOS ============ -->
<section class="servicios">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Lo que nos define</p>
      <h2 class="h2">Tres compromisos <em>con cada cliente.</em></h2>
    </div>
    <ul class="serv-grid">
      <li class="serv reveal"><i class="ti ti-user-check"></i><h3>Trato directo</h3><p>Tu caso lo atienden los profesionales del estudio, sin intermediarios ni derivaciones.</p></li>
      <li class="serv reveal"><i class="ti ti-clock-hour-4"></i><h3>Respuesta en 24 horas</h3><p>Contestamos cada consulta en menos de un día hábil, con un primer panorama claro de tu situación.</p></li>
      <li class="serv reveal"><i class="ti ti-file-text"></i><h3>Honorarios claros</h3><p>Presupuesto escrito y detallado antes de iniciar cualquier trámite.</p></li>
    </ul>
  </div>
</section>

<!-- ============ EQUIPO ============ -->
<section class="equipo">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Nuestro equipo</p>
      <h2 class="h2">Dos generaciones, <em>un mismo equipo.</em></h2>
    </div>
    <div class="dupla dupla-full">
      <article class="reveal">
        <span class="dupla-n">+20</span>
        <h3>Abogados con trayectoria</h3>
        <p>Profesionales con décadas de ejercicio, que conocen la jurisprudencia, los tribunales y los pliegues del trámite. Aportan criterio, prudencia y la solidez que solo da el tiempo.</p>
        <ul class="dupla-list">
          <li>Más de 20 años de ejercicio ininterrumpido</li>
          <li>Dominio de la jurisprudencia y del fuero local</li>
          <li>Criterio forjado en casos reales</li>
        </ul>
      </article>
      <div class="eje-v" aria-hidden="true"></div>
      <article class="reveal">
        <span class="dupla-n"><i class="ti ti-device-laptop"></i></span>
        <h3>Abogados de nueva generación</h3>
        <p>Profesionales que dominan los procesos digitales: expedientes electrónicos, presentaciones a distancia y herramientas que acortan tiempos. Aportan rapidez, orden y transparencia.</p>
        <ul class="dupla-list">
          <li>Manejo fluido de expedientes digitales</li>
          <li>Trámites a distancia, sin traslados innecesarios</li>
          <li>Seguimiento del caso en tiempo real</li>
        </ul>
      </article>
    </div>
    <blockquote class="cita reveal">
      <p>Experiencia y rapidez, <em>en el mismo equipo.</em></p>
      <footer>El criterio de quienes vieron muchas causas, con la eficiencia de quienes crecieron con la tecnología.</footer>
    </blockquote>
  </div>
</section>

<!-- ============ MÉTODO ============ -->
<section class="metodo metodo-d" id="metodo">
  <div class="wrap">
    <div class="sec-head reveal">
      <p class="eyebrow">Nuestro método</p>
      <h2 class="h2">Tu tranquilidad empieza <em>con información clara.</em></h2>
      <p class="lead">Tres pilares: análisis riguroso, plazos concretos y comunicación permanente.</p>
    </div>
    <ol class="eje eje-largo" id="eje">
{eje}
    </ol>
  </div>
</section>

<!-- ============ POR QUÉ ============ -->
<section class="faq">
  <div class="wrap faq-grid">
    <div class="reveal">
      <p class="eyebrow">Por qué elegirnos</p>
      <h2 class="h2">Más que escritos <em>y trámites.</em></h2>
      <p class="lead">Un buen servicio jurídico también es escuchar, explicar, planificar y mantener informado al cliente.</p>
    </div>
    <ul class="pq-list reveal">
      <li><i class="ti ti-calendar-time"></i><div><b>Plazos concretos</b><span>Sabés cuándo recibís el presupuesto y cuándo empezamos.</span></div></li>
      <li><i class="ti ti-message-circle"></i><div><b>Información clara</b><span>Te explicamos las etapas del proceso y lo relevante de tu caso.</span></div></li>
      <li><i class="ti ti-report"></i><div><b>Seguimiento semanal</b><span>Informes por email o WhatsApp, sin tener que preguntar.</span></div></li>
      <li><i class="ti ti-map-pin"></i><div><b>Atención personalizada</b><span>Primera entrevista presencial en CABA o virtual.</span></div></li>
      <li><i class="ti ti-users-group"></i><div><b>Trabajo en equipo</b><span>Cada caso se analiza de manera coordinada entre los integrantes del estudio.</span></div></li>
    </ul>
  </div>
</section>
''' + cta_band(("Tu caso merece atención,", "claridad y compromiso."), "Coordiná tu primera entrevista, presencial o virtual, y conocé cómo podemos trabajar en tu caso.", WA_DEF) + "\n</main>\n" + FOOTER + tail()
write("estudio.html", estudio)

# ------------------------------------------------------------------ preguntas frecuentes
side = "\n".join(f'        <li><a href="#{a["slug"]}"><span>{a["n"]}</span>{a["name"]}</a></li>' for a in AREAS)
groups = []
faq_ld = []
for a in AREAS:
    qs = FAQ[a["slug"]]
    faq_ld += [{"@type": "Question", "name": q[0], "acceptedAnswer": {"@type": "Answer", "text": q[1]}} for q in qs]
    if len(qs[0]) == 3:  # con subtemas
        body, cur = [], None
        for q in qs:
            if q[2] != cur:
                if cur is not None:
                    body.append("      </ul>")
                cur = q[2]
                body.append(f'      <h3 class="faq-sub">{cur}</h3>\n      <ul class="faq-list">')
            body.append(faq_items([(q[0], q[1])]))
        body.append("      </ul>")
        inner = "\n".join(body)
    else:
        inner = '      <ul class="faq-list">\n' + faq_items(qs) + "\n      </ul>"
    groups.append(f'''    <section class="faq-grp" id="{a["slug"]}">
      <div class="faq-grp-head">
        <h2><span>{a["n"]}</span>{a["name"]}</h2>
        <a href="./{a["slug"]}.html" class="link-arrow">Ver el área <i class="ti ti-arrow-right"></i></a>
      </div>
{inner}
    </section>''')
pf = head("Preguntas frecuentes | Sucesiones, penal, laboral y más | Axis Legal",
  "Respuestas claras a las consultas legales más habituales sobre sucesiones, derecho penal, laboral, accidentes de tránsito, amparos de salud, comercial e inmobiliario.",
  {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": faq_ld}) + header("preguntas-frecuentes.html") + "\n<main>\n" + page_hero(
  "biblioteca", "center 40%", [("Preguntas frecuentes", None)], ("Respuestas claras", "a tus dudas legales."),
  "Reunimos las consultas más habituales, organizadas por área. Si no encontrás tu respuesta, escribinos y un profesional del estudio te responde en menos de 24 horas hábiles.", pxkey="biblioteca") + f'''
<!-- ============ PREGUNTAS POR ÁREA ============ -->
<section class="faqp">
  <div class="wrap faqp-grid">
    <aside class="faqp-side">
      <p class="eyebrow">Áreas</p>
      <ul>
{side}
      </ul>
    </aside>
    <div class="faqp-main">
{chr(10).join(groups)}
      <p class="faq-note">La información de este sitio es orientativa y no reemplaza el asesoramiento sobre tu caso.</p>
    </div>
  </div>
</section>
''' + cta_band(("¿No encontraste", "tu respuesta?"), "Cada caso es único. Escribinos y un abogado del estudio te responde en menos de 24 horas hábiles.", WA_DEF) + "\n</main>\n" + FOOTER + tail()
write("preguntas-frecuentes.html", pf)

# ------------------------------------------------------------------ privacidad
priv = head("Política de privacidad | Axis Legal", "Cómo trata Axis Legal los datos personales que recibe a través de este sitio, conforme a la Ley 25.326 de Protección de Datos Personales.") + header() + "\n<main>\n" + page_hero(
  None, "", [("Política de privacidad", None)], ("Política", "de privacidad."), "Cómo tratamos los datos que nos enviás a través de este sitio.", short=True) + '''
<section class="legal">
  <div class="wrap legal-in">
    <p class="legal-date">Última actualización: octubre de 2026</p>

    <h2>1. Responsable</h2>
    <p>El responsable del tratamiento de los datos es Axis Legal, con domicilio en Adolfo Alsina 1609, oficina 26, Ciudad Autónoma de Buenos Aires. Podés contactarnos por WhatsApp al 11 5846-5239 o en el estudio, de lunes a viernes de 10 a 17 h.</p>

    <h2>2. Qué datos recopilamos</h2>
    <p>Solo los que nos enviás voluntariamente: tu nombre, email, teléfono (opcional), el área legal de interés y el mensaje que escribís en el formulario de contacto, o los datos que compartís al escribirnos por WhatsApp. El sitio no usa cookies de seguimiento ni herramientas de publicidad.</p>

    <h2>3. Para qué los usamos</h2>
    <p>Para responder tu consulta, coordinar una entrevista y, si decidís contratarnos, prestar el servicio. No usamos tus datos para otros fines ni los cedemos a terceros con fines comerciales.</p>

    <h2>4. Secreto profesional</h2>
    <p>Toda la información que nos confiás está protegida por el secreto profesional que rige el ejercicio de la abogacía.</p>

    <h2>5. Servicios de terceros</h2>
    <p>Para funcionar, el sitio usa servicios externos que pueden procesar datos técnicos (como la dirección IP):</p>
    <ul>
      <li><b>FormSubmit</b>, que envía a nuestro correo los datos del formulario de contacto.</li>
      <li><b>WhatsApp</b> (Meta Platforms), si elegís escribirnos por ese medio.</li>
      <li><b>Google Fonts</b> y <b>jsDelivr</b>, que sirven las tipografías y los íconos del sitio.</li>
    </ul>
    <p>Cada uno se rige por su propia política de privacidad.</p>

    <h2>6. Conservación y seguridad</h2>
    <p>Conservamos los datos el tiempo necesario para atender tu consulta y cumplir obligaciones legales y profesionales, y aplicamos medidas razonables para protegerlos.</p>

    <h2>7. Tus derechos</h2>
    <p>Conforme a la Ley 25.326, podés solicitar en forma gratuita el acceso, la rectificación, la actualización o la supresión de tus datos, contactándonos por los medios indicados en el punto 1. La Agencia de Acceso a la Información Pública, órgano de control de la Ley 25.326, atiende las denuncias y los reclamos por incumplimientos de las normas sobre protección de datos personales.</p>

    <h2>8. Cambios</h2>
    <p>Podemos actualizar esta política. La versión vigente es siempre la publicada en esta página.</p>
  </div>
</section>
''' + "\n</main>\n" + FOOTER + tail()
write("privacidad.html", priv)

# ------------------------------------------------------------------ 404
nf = head("Página no encontrada | Axis Legal", "La página que buscás no existe o cambió de dirección.", robots="noindex") + header() + f'''
<main>
<section class="nf">
  <div class="nf-bg" aria-hidden="true"></div>
  <div class="wrap nf-in">
    <span class="nf-num" aria-hidden="true">404</span>
    <h1 class="ph-h1">Esta página <em>no existe.</em></h1>
    <p class="lead">Puede que haya cambiado de dirección. Volvé al inicio o escribinos y te ayudamos.</p>
    <div class="ph-ctas">
      <a class="btn btn-gold" href="./index.html">Volver al inicio</a>
      <a class="btn btn-line js-wa" href="#" data-msg="{WA_DEF}">Consultar por WhatsApp</a>
    </div>
  </div>
</section>
</main>
''' + FOOTER + tail()
write("404.html", nf)
