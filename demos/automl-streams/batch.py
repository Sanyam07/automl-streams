from automlstreams.streams import KafkaStream
from automlstreams.evaluators import EvaluatePretrained

from sklearn.ensemble import GradientBoostingClassifier

DEFAULT_INPUT_TOPIC = 'sea_big'
DEFAULT_BROKER = 'broker:29092'
BATCH_SIZE = 5000
MAX_SAMPLES = 10000


def run(topic=DEFAULT_INPUT_TOPIC, broker=DEFAULT_BROKER):
    print(f'Running demo for topic={topic} and broker={broker}')
    stream = KafkaStream(topic, bootstrap_servers=broker)
    stream.prepare_for_use()

    # Get a batch of BATCH_SIZE samples
    X, y = stream.next_sample(BATCH_SIZE)
    print('Sampled batch shape: ', X.shape)

    model = GradientBoostingClassifier()

    model.fit(X, y)

    evaluator = EvaluatePretrained(show_plot=False,
                                   n_wait=200,
                                   batch_size=1,
                                   max_samples=MAX_SAMPLES,
                                   output_file=f'results/batch_{topic}.csv')

    evaluator.evaluate(stream=stream, model=model)


if __name__ == "__main__":
    topics = ['elec', 'covtype', 'weather', 'sea_big', 'moving_squares']
    for topic in topics:
        run(topic)