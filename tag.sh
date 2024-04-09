cd frontend/

docker build . -t district-party-frontend

cd ../backend

docker build . -t district-party-backend

cd ../

docker tag district-party-frontend \
    us-central1-docker.pkg.dev/district-party/district-party-repository/district-party-frontend

docker push us-central1-docker.pkg.dev/district-party/district-party-repository/district-party-frontend

docker tag district-party-backend \
    us-central1-docker.pkg.dev/district-party/district-party-repository/district-party-backend

docker push us-central1-docker.pkg.dev/district-party/district-party-repository/district-party-backend

