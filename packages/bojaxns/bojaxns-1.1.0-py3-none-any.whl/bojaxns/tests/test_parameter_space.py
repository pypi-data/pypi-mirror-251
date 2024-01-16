from jax import vmap, random, numpy as jnp
from jaxns.framework.ops import parse_prior, transform
from jaxns.internals.types import float_type

from bojaxns.common import FloatValue, IntValue
from bojaxns.parameter_space import IntegerPrior, CategoricalPrior, ParameterSpace, \
    Parameter, build_prior_model, ContinuousPrior, sample_U_value
from bojaxns.utils import build_example


def test_serialisation():
    for m in [
        IntegerPrior,
        CategoricalPrior,
        ContinuousPrior
    ]:
        s = build_example(m)
        assert s == m.parse_raw(s.json())


def test_build_prior():
    def _sample_prior(key, prior_model):
        U_placeholder, X_placeholder = parse_prior(prior_model=prior_model)
        U_ndims = U_placeholder.size
        U = random.uniform(key=key, shape=(U_ndims,), dtype=float_type)
        X = transform(U=U, prior_model=prior_model)
        return X

    parameter_space = ParameterSpace(parameters=[
        Parameter(
            name='continuous',
            prior=ContinuousPrior(
                lower=0.,
                upper=5.,
                mode=4.,
                uncert=1.3
            )
        ),
        Parameter(
            name='integers',
            prior=IntegerPrior(
                lower=0,
                upper=5,
                mode=4.,
                uncert=1.3
            )
        ),
        Parameter(
            name='categorical',
            prior=CategoricalPrior(
                probs=[1., 1., 1.]
            )
        )
    ])
    prior_model = build_prior_model(parameter_space=parameter_space)

    X = vmap(lambda key: _sample_prior(key=key, prior_model=prior_model))(random.split(random.PRNGKey(42), 1000))

    x = X['continuous']
    assert jnp.all(x >= 0.)
    assert jnp.all(x <= 5.)
    assert jnp.any(x < 1.)
    assert jnp.any(x > 4.)

    x = X['integers']

    assert jnp.all(x >= 0)
    assert jnp.all(x <= 5)
    assert jnp.any(x == 0)
    assert jnp.any(x == 5)

    x = X['categorical']
    assert jnp.all(x >= 0)
    assert jnp.all(x <= 2)
    assert jnp.any(x == 0)
    assert jnp.any(x == 1)
    assert jnp.any(x == 2)


def test_decision_variable():
    def _sample_prior(key, prior_model):
        U_placeholder, X_placeholder = parse_prior(prior_model=prior_model)
        U_ndims = U_placeholder.size
        U = random.uniform(key=key, shape=(U_ndims,), dtype=float_type)
        X = transform(U=U, prior_model=prior_model)
        return X

    parameter_space = ParameterSpace(parameters=[
        Parameter(
            name='categorical',
            prior=CategoricalPrior(
                probs=[1., 1.]
            )
        )
    ])
    prior_model = build_prior_model(parameter_space=parameter_space)

    X = vmap(lambda key: _sample_prior(key=key, prior_model=prior_model))(random.split(random.PRNGKey(42), 1000))

    x = X['categorical']
    assert jnp.all(x >= 0)
    assert jnp.all(x <= 1)
    assert jnp.any(x == 0)
    assert jnp.any(x == 1)


def test_close_to_zero():
    def _sample_prior(key, prior_model):
        U_placeholder, X_placeholder = parse_prior(prior_model=prior_model)
        U_ndims = U_placeholder.size
        U = random.uniform(key=key, shape=(U_ndims,), dtype=float_type)
        X = transform(U=U, prior_model=prior_model)
        return X

    parameter_space = ParameterSpace(parameters=[
        Parameter(
            name='churn_rate',
            prior=ContinuousPrior(
                lower=1 / 20.,
                upper=1 / 10.,
                mode=1 / 15.,
                uncert=1 / 15.
            )
        )
    ])

    prior_model = build_prior_model(parameter_space=parameter_space)

    X = vmap(lambda key: _sample_prior(key=key, prior_model=prior_model))(random.split(random.PRNGKey(42), 1000))

    x = X['churn_rate']
    assert jnp.all(x >= 1 / 20)
    assert jnp.all(x <= 1 / 10)


def test_parameter_space():
    param1 = Parameter(
        name='continuous',
        prior=build_example(ContinuousPrior)
    )

    param2 = Parameter(
        name='integers',
        prior=build_example(IntegerPrior)
    )

    param3 = Parameter(
        name='categorical',
        prior=build_example(CategoricalPrior)
    )

    _ = ParameterSpace(parameters=[param1, param2, param3])
    try:
        _ = ParameterSpace(parameters=[param1, param1])
        assert False
    except ValueError as e:
        assert 'parameter names must be unique' in str(e)


def test_sample_U_value():
    param1 = Parameter(
        name='continuous',
        prior=build_example(ContinuousPrior)
    )

    param2 = Parameter(
        name='integers',
        prior=build_example(IntegerPrior)
    )

    param3 = Parameter(
        name='categorical',
        prior=build_example(CategoricalPrior)
    )

    parameter_space = ParameterSpace(parameters=[param1, param2, param3])

    param_values = {
        'continuous': FloatValue(value=param1.prior.lower),
        'integers': IntValue(value=param2.prior.lower),
        'categorical': IntValue(value=0)
    }
    U_sample = sample_U_value(key=random.PRNGKey(42), param_space=parameter_space,
                              param_values=param_values)

    prior_model = build_prior_model(parameter_space=parameter_space)
    X = transform(U=jnp.asarray(U_sample), prior_model=prior_model)
    for key in X:
        assert jnp.allclose(X[key], param_values[key].value)

    param_values = {
        'continuous': FloatValue(value=param1.prior.upper),
        'integers': IntValue(value=param2.prior.upper),
        'categorical': IntValue(value=0)
    }
    U_sample = sample_U_value(key=random.PRNGKey(42), param_space=parameter_space,
                              param_values=param_values)

    prior_model = build_prior_model(parameter_space=parameter_space)
    X = transform(U=jnp.asarray(U_sample), prior_model=prior_model)
    for key in X:
        assert jnp.allclose(X[key], param_values[key].value)
